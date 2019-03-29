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
  public vitals = [];
  public searchInput = '';
  public vitalsShown = [];
  public selectedVital = null;
  public editingTemplate = false;
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
      this.editingTemplate = this.data.editingTemplate;
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
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
    let filtered = this.vitals.filter(
      (obj) => obj.name === vital.name
    ).filter(
      (obj) => obj.is_active === true
    );
    return filtered.length;
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

  public createNewVital() {
    this.store.VitalsTaskTemplate.create({
      plan_template: this.data.planTemplateId,
      start_on_day: 0,
      appear_time: '00:00:00',
      due_time: '00:00:00',
      name: this.newVitalName,
    }).subscribe(
      (vitalTemplate) => {
        this.vitals.push(vitalTemplate);
        this.createVital = false;
        this.modalRespData.nextAction = 'createVital';
        this.modalRespData.data = vitalTemplate;
        this.modal.close(this.modalRespData);
      },
      (err) => {},
      () => {}
    );
  }

  public openFullPreview(vital) {
    this.modalRespData.nextAction = 'fullVitalPreview';
    this.modalRespData.data = this.selectedVital;
    this.modal.close(this.modalRespData);
  }

  public clickNext() {
    let newVital = {
      start_on_day: 0,
      appear_time: '00:00:00',
      due_time: '00:00:00',
      name: this.selectedVital.name,
      instructions: this.selectedVital.instructions,
      plan_template: this.data.planTemplateId,
    };
    let createSub = this.store.VitalsTaskTemplate.create(newVital).subscribe(
      (resp) => {
        this.vitals.push(resp);
        this.createVital = false;
        this.selectedVital.questions.forEach((question, i, array) => {
          let updatedQuestion = _omit(question, 'id');
          updatedQuestion.vital_task_template = resp.id;
          this.store.VitalsQuestions.create(updatedQuestion).subscribe((newQuestion) => {
            resp.questions.push(newQuestion);
            if (i === array.length - 1) {
              this.modalRespData.nextAction = 'createVital';
              this.modalRespData.data = resp;
              this.modal.close(this.modalRespData);
            }
          });
        });
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      }
    );
  }

  public clickClose() {
    this.modal.close(null);
  }
}
