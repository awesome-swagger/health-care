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
  public vitalTemplatePreview: object = {vital:{},vitals:[]};
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

  private exampleData: object = {
   
      "id": "6b6df74f-1f39-44ef-8555-81f0a9aa8923",
      "plan_template": "719563fb-6394-47b8-89e0-3f6f4fad9c9f",
      "name": "Sleep Report",
      "start_on_day": 0,
      "frequency": "daily",
      "repeat_amount": -1,
      "appear_time": "01:00:00",
      "due_time": "15:03:00"
  };
  constructor(
    private modal: ModalService,
    private store: StoreService
  ) {
  
  }
  public ngOnInit() {
    console.log(this.data);
    this.vitalTemplates = this.data;
  }

  public close() {
    this.modal.close(null);
  }

  public showVitalPreview(vital) {
    this.vitalTemplatePreview['vital'] = vital;
    this.store.VitalsQuestions.readListPaged({vital_task_template: vital.id}).subscribe((resp)=>{
      this.vitalTemplatePreview['vitals'] = resp;
    })
  }

  public editVitalTemplate(e,vital) {
    e.stopPropagation();
    this.modalRespData.nextAction = 'editVital';
    this.modalRespData.data = this.vitalTemplatePreview;
    this.modal.close(this.modalRespData);  
  }

  public openFullPreview(vital) {
    this.modalRespData.nextAction = 'fullVitalPreview';
    this.modalRespData.data = this.vitalTemplatePreview;
    this.modal.close(this.modalRespData);
  }


}
