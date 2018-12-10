import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import {
  AddAssessmentComponent,
  AddCTTaskComponent,
  AddStreamComponent,
  AddVitalComponent,
  EditTaskComponent,
  GoalComponent,
  PreviewVitalComponent,
  CreateVitalComponent,
} from '../../../components';
import { NavbarService, StoreService } from '../../../services';

@Component({
  selector: 'app-plan-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.scss'],
})
export class PlanScheduleComponent implements OnDestroy, OnInit {

  public planTemplateId = null;
  public planTemplate = null;
  public goalTemplates = [];
  public teamTaskTemplates = [];
  public teamManagerTemplates = [];
  public teamMemberTemplates = [];
  public patientTaskTemplates = [];
  public symptomTemplates = [];
  public assessmentTemplates = [];
  public vitalTemplates = [];
  public messageQueues = [];

  public accordionsOpen = [];
  public tooltipsOpen = [];

  public toolPTAOpen;
  public toolPTA2Open
  public toolPTA3Open;
  public planAssessements;
  public toolPTSOpen;
  public toolPTVOpen;
  public toolPTMOpen;

  constructor(
    private route: ActivatedRoute,
    private modals: ModalService,
    private nav: NavbarService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.planTemplateId = params.id;
      this.nav.planDetailState(this.planTemplateId);
      this.store.CarePlanTemplate.read(this.planTemplateId).subscribe((planTemplate) => {
        this.planTemplate = planTemplate;
      });
    });
    this.store.GoalTemplate.readListPaged({
      plan_template: this.planTemplateId,
    }).subscribe((goals) => {
      this.goalTemplates = goals;
    });
    this.store.TeamTaskTemplate.readListPaged({
      plan_template: this.planTemplateId,
    }).subscribe((teamTaskTemplates) => {
      this.teamTaskTemplates = teamTaskTemplates;
      this.teamManagerTemplates = teamTaskTemplates.filter(task => task.is_manager_task);
      this.teamMemberTemplates = teamTaskTemplates.filter(task => !task.is_manager_task);
    });
    this.store.SymptomTaskTemplate.readListPaged({
      plan_template: this.planTemplateId,
    }).subscribe((symptoms) => {
      this.symptomTemplates = symptoms;
    });
    this.store.InfoMessageQueue.readListPaged({
      plan_template: this.planTemplateId,
    }).subscribe((messages) => {
      this.messageQueues = messages;
    });
    this.store.VitalsTaskTemplate.readListPaged({
      plan_template: this.planTemplateId,
    }).subscribe((vitals) => {
      this.vitalTemplates = vitals;
    });
    this.store.PatientTaskTemplate.readListPaged({
      plan_template: this.planTemplateId,
    }).subscribe((patientTasks) => {
      this.patientTaskTemplates = patientTasks;
    });
    this.store.AssessmentTaskTemplate.readListPaged({
      plan_template: this.planTemplateId,
    }).subscribe((assessments) => {
      this.assessmentTemplates = assessments;
    });
  }

  public ngOnDestroy() { }

  public openGoal() {
    this.modals.open(GoalComponent, {
      closeDisabled: true,
      data: {
        creatingTemplate: true,
      },
      width: '512px',
    }).subscribe((results) => {
      if (results !== null) {
        this.store.GoalTemplate.create({
          name: results.name,
          plan_template: this.planTemplateId,
          description: results.description,
          focus: results.focus,
          duration_weeks: results.duration_weeks,
          start_on_day: results.start_on_day,
        }).subscribe((goal) => {});
      }
    });
  }

  public editGoal(goal) {
    this.modals.open(GoalComponent, {
      closeDisabled: true,
      data: {
        creatingTemplate: false,
        goalTemplate: goal,
      },
      width: '512px',
    }).subscribe((results) => {
      if (results !== null) {
        this.store.GoalTemplate.update(goal.id, {
          name: results.name,
          description: results.description,
          focus: results.focus,
          duration_weeks: results.duration_weeks,
          start_on_day: results.start_on_day,
        }, true).subscribe((goal) => {});
      }
    });
  }

  public confirmDeleteGoal() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Goal?',
       body: 'Are you sure you want to delete this care plan goal? This will affect X patients currently assigned to this care plan.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe((result) => {
      console.log(result);
    });
  }

  public addCTTask() {
    this.modals.open(AddCTTaskComponent, {
      closeDisabled: true,
      width: '384px',
      data: {careTeamTasks:this.teamTaskTemplates, planTemplateId: this.planTemplateId},
    }).subscribe((data) => {
      if (data !== null) {
        this.editCTTask(data);
      }
    });
  }

  public editCTTask(data) {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
      data: data,
    }).subscribe((resp) => {
      console.log(resp);
    });
  }

  public confirmDeleteCTTask(task) {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Task?',
       body: 'Are you sure you want to remove this task? This will affect X patients currently assigned to this care plan.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe((data) => {
      if (data = 'Continue') {
        this.store.TeamTaskTemplate.destroy(task.id).subscribe((resp)=>{
          this.teamTaskTemplates = this.teamTaskTemplates.filter(item => item.id == task.id);
        });
      }
    });
  }

  public addTask() {
    this.modals.open(AddCTTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public editTask() {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public confirmDeleteTask() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Task?',
       body: 'Are you sure you want to remove this task? This will affect X patients currently assigned to this care plan.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe((resp) => {});
  }

  public addAssessment() {
    this.modals.open(AddAssessmentComponent, {
      closeDisabled: true,
      width: '768px',
    }).subscribe(() => {});
  }

  public editAssessment() {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public confirmDeleteAssessment() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Assessment?',
       body: 'Are you sure you want to remove this assessment? This will affect X patients currently assigned to this care plan.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {});
  }

  public addSymptom() {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public editSymptom() {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public confirmDeleteSymptom() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Symptom Report?',
       body: 'Are you sure you want to remove this symptom report? This will affect X patients currently assigned to this care plan.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {});
  }

  public addVital(vitalTemplates) {
    this.modals.open(AddVitalComponent, {
      closeDisabled: true,
      width: '768px',
      data: vitalTemplates
    }).subscribe((data) => {
      switch(data.nextAction)
      {
        case 'fullVitalPreview':
            this.previewVital(data.data);
            break;
        case 'editVital':
            this.editVital(data.data);
            break;
        default:
             break;
      }

    });
  }

  public editVital(vital) {
    this.modals.open(CreateVitalComponent, {
      closeDisabled: true,
      width: '800px',
      data: vital
    }).subscribe(() => {});
  }
  public previewVital(vital) {
    this.modals.open(PreviewVitalComponent, {
      closeDisabled: true,
      width: '500px',
      data: vital
    }).subscribe(() => {});
  }

  public confirmDeleteVital() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Vital?',
       body: 'Are you sure you want to remove this vital report? This will affect X patients currently assigned to this care plan.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {});
  }

  public addStream() {
    this.modals.open(AddStreamComponent, {
      closeDisabled: true,
      width: '768px',
    }).subscribe(() => {});
  }

  public editStream() {
    this.modals.open(AddStreamComponent, {
      closeDisabled: true,
      width: '768px',
    }).subscribe(() => {});
  }

  public confirmDeleteStream() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Message Stream?',
       body: 'Are you sure you want to remove this message stream? This will affect X patients currently assigned to this care plan.',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {});
  }
}
