import { Component, OnInit } from '@angular/core';import {
  groupBy as _groupBy,
  uniqBy as _uniqBy,
  omit as _omit,
} from 'lodash';
import { StoreService } from '../../../services';
import { ModalService } from '../../../modules/modals';

@Component({
  selector: 'app-add-vital',
  templateUrl: './add-vital.component.html',
  styleUrls: ['./add-vital.component.scss'],
})
export class AddVitalComponent implements OnInit {

  public data = null;
  public totalPatients = 0;
  public isAdhoc = false;
  public vitals = [];
  public searchInput = '';
  public vitalsShown = [];
  public selectedVital = null;
  public createVital = false;
  public newVitalName = '';
  private modalRespData = {
    nextAction: null,
    data: null
  };
  public vital;

  constructor(
    private modal: ModalService,
    private store: StoreService
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
      if (this.data.planTemplateId) {
        this.isAdhoc = false;
      } else if (this.data.planId) {
        this.isAdhoc = true;
      }
      this.store.VitalsTaskTemplate.readListPaged({
        is_available: true,
      }).subscribe(
        (data) => {
          this.vitals = data;
          this.vitalsShown = _uniqBy(this.vitals, (obj) => {
            return obj.name;
          });
        },
        (err) => {},
        () => {}
      );
    }
  }

  public filterVitals() {
    let vitalMatches = this.vitals.filter((obj) => {
      return obj.name.toLowerCase().indexOf(this.searchInput.toLowerCase()) >= 0;
    });
    this.vitalsShown = _uniqBy(vitalMatches, (obj) => obj.name);
  }

  public showVitalPreview(vital) {
    this.selectedVital = vital;
  }

  public uniqByNameCount(vital) {
    let uniqueVitals = this.vitals.filter(
      (obj) => obj.name === vital.name
    ).filter(
      (obj) => obj.is_active === true
    );
    return uniqueVitals.length;
  }

  public clickEditVital(vital, e) {
    e.stopPropagation();
    vital.edit = !vital.edit;
    vital.origName = vital.name;
  }

  public clickUndoName(vital, e) {
    e.stopPropagation();
    vital.edit = !vital.edit;
    vital.name = vital.origName;
  }

  public updateVitalName(vital, e) {
    e.stopPropagation();
    let vitals = this.vitals.filter((obj) => obj.name === vital.origName || obj.name === vital.name);
    vitals.forEach((obj) => {
      let updateSub = this.store.VitalsTaskTemplate.update(obj.id, {
        name: vital.name,
      }, true).subscribe(
        (resp) => {
          obj.name = vital.name;
          vital.edit = false;
        },
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
    });
  }

  public clickDeleteVital(vital, e) {
    e.stopPropagation();
    vital.delete = true;
  }

  public clickUndoDelete(vital, e) {
    e.stopPropagation();
    vital.delete = false;
  }

  public confirmDeleteVital(vital, e) {
    e.stopPropagation();
    let vitals = this.vitals.filter((obj) => obj.name === vital.origName || obj.name === vital.name);
    vitals.forEach((obj) => {
      let updateSub = this.store.VitalsTaskTemplate.update(obj.id, {
        is_available: false,
        is_active: false
      }, true).subscribe(
        (resp) => {
          let index = this.vitals.findIndex((a) => a.id === resp.id);
          this.vitals.splice(index, 1);
          vital.delete = false;
          this.vitalsShown = _uniqBy(this.vitals, (obj) => {
            return obj.name;
          });
        },
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
    });
  }

  public createNewVital(vitalName) {
    if (vitalName.length <= 0) {
      return;
    }
    let newVital = {};
    if (!this.isAdhoc) {
      newVital = {
        start_on_day: 0,
        frequency: 'once',
        repeat_amount: -1,
        appear_time: '00:00:00',
        due_time: '00:00:00',
        is_active: true,
        is_available: true,
        name: vitalName,
        plan_template: this.data.planTemplateId,
        instructions: '',
      }
      this.createVital = false;
      this.modal.close({
        nextAction: 'createVital',
        data: newVital
      });
    } else {
      newVital = {
        start_on_day: 0,
        frequency: 'once',
        repeat_amount: -1,
        appear_time: '00:00:00',
        due_time: '00:00:00',
        name: vitalName,
        plan: this.data.planId,
        instructions: '',
      };
      this.createVital = false;
      this.modal.close({
        nextAction: 'createVital',
        data: newVital
      });
    }
  }

  public openFullPreview(vital) {
    this.modalRespData.nextAction = 'fullVitalPreview';
    this.modalRespData.data = this.selectedVital;
    this.modal.close(this.modalRespData);
  }

  public clickNext() {
    let newVital: any = {};
    newVital = {
      start_on_day: this.selectedVital.start_on_day,
      frequency: this.selectedVital.frequency,
      repeat_amount: this.selectedVital.repeat_amount,
      appear_time: this.selectedVital.appear_time,
      due_time: this.selectedVital.due_time,
      name: this.selectedVital.name,
      is_active: true,
      is_available: true,
      instructions: this.selectedVital.instructions,
    };
    if (!this.isAdhoc) {
      newVital['plan_template'] = this.data.planTemplateId;
    } else {
      newVital['plan'] = this.data.planId;
      newVital['vital_task_template'] = this.selectedVital;
    }
    newVital['questions'] = this.selectedVital.questions.map((obj) => {
      return _omit(_omit(obj, 'id'), 'vital_task_template');
    });
    this.createVital = false;
    this.modal.close({
      nextAction: 'createVital',
      data: newVital,
    });
  }

  public clickClose() {
    this.modal.close(null);
  }
}
