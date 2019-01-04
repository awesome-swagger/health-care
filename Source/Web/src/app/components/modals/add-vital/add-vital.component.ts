import { Component, OnInit } from '@angular/core';
import { StoreService } from '../../../services';
import { ModalService } from '../../../modules/modals';

@Component({
  selector: 'app-add-vital',
  templateUrl: './add-vital.component.html',
  styleUrls: ['./add-vital.component.scss'],
})
export class AddVitalComponent implements OnInit {

  public data = null;
  public vitalTemplates: Array<any> = [];
  public searchInput = '';
  public vitalTemplatesShown = [];
  public vitalTemplatePreview = {
    vital: null,
    vitals: []
  };
  public createVital = false;
  public newVitalName = '';
  private modalRespData = {
    nextAction: null,
    data:null
  }
  private minimumData: object = {
    name:'',
    start_on_day:0,
    appear_time:'',
    due_time:''
  };
  public vital;

  constructor(
    private modal: ModalService,
    private store: StoreService
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.vitalTemplates = this.data.taskList;
      this.vitalTemplatesShown = this.vitalTemplates;
    }
  }

  public filterVitals() {
    this.vitalTemplatesShown = this.vitalTemplates.filter((obj) => {
      return obj.name.toLowerCase().indexOf(this.searchInput.toLowerCase()) >= 0;
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
        this.modalRespData.nextAction = 'editVital';
        this.modalRespData.data = vitalTemplate;
        this.modal.close(this.modalRespData);
      },
      (err) => {},
      () => {}
    );
  }

  public showVitalPreview(vital) {
    this.vitalTemplatePreview['vital'] = vital;
    this.store.VitalsQuestions.readListPaged({
      vital_task_template: vital.id
    }).subscribe((resp) => {
      this.vitalTemplatePreview['vitals'] = resp;
    })
  }

  public editVitalTemplate(e, vital) {
    e.stopPropagation();
    this.modalRespData.nextAction = 'editVital';
    this.modalRespData.data = this.vitalTemplatePreview.vital;
    this.modal.close(this.modalRespData);
  }

  public openFullPreview(vital) {
    this.modalRespData.nextAction = 'fullVitalPreview';
    this.modalRespData.data = this.vitalTemplatePreview.vital;
    this.modal.close(this.modalRespData);
  }

  public close() {
    this.modal.close(null);
  }
}
