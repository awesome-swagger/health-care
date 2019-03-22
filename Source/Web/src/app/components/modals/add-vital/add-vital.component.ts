import { Component, OnInit } from '@angular/core';import {
  groupBy as _groupBy,
  uniqBy as _uniqBy,
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
      this.store.VitalsTaskTemplate.readListPaged().subscribe(
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

  public uniqByNameCount(vital) {
    return this.vitals.filter((obj) => obj.name === vital.name).length;
  }

  public filterVitals() {
    let vitalMatches = this.vitals.filter((obj) => {
      return obj.name.toLowerCase().indexOf(this.searchInput.toLowerCase()) >= 0;
    });
    this.vitalsShown = _uniqBy(vitalMatches, (obj) => obj.name);
  }

  public clickEditVital(vital, e) {
    e.stopPropagation();
    vital.edit = !vital.edit;
    vital.origName = vital.name;
  }

  public clickDeleteVital(vital, e) {
    e.stopPropagation();
  }

  public clickUndoName(vital, e) {
    e.stopPropagation();
    vital.edit = !vital.edit;
    vital.name = vital.origName;
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

  public showVitalPreview(vital) {
    this.selectedVital = vital;
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
      plan_template: this.data.planTemplateId,
    };
    let createSub = this.store.VitalsTaskTemplate.create(newVital).subscribe(
      (resp) => {
        this.vitals.push(resp);
        this.modalRespData.nextAction = 'createVital';
        this.modalRespData.data = resp;
        this.modal.close(this.modalRespData);
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
