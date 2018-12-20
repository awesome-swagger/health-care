import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import {
  AddAssessmentComponent,
  AddCTTaskComponent,
  AddStreamComponent,
  AddVitalComponent,
  CreateAssessmentComponent,
  EditTaskComponent,
  GoalComponent,
  PreviewVitalComponent,
  CreateVitalComponent,
  PlanDurationComponent,
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
      this.store.GoalTemplate.readListPaged({
        plan_template__id: this.planTemplateId,
      }).subscribe((goals) => {
        this.goalTemplates = goals;
      });
      this.store.TeamTaskTemplate.readListPaged({
        plan_template__id: this.planTemplateId,
      }).subscribe((teamTaskTemplates) => {
        this.teamTaskTemplates = teamTaskTemplates;
        this.teamManagerTemplates = teamTaskTemplates.filter((task) => task.is_manager_task);
        this.teamMemberTemplates = teamTaskTemplates.filter((task) => !task.is_manager_task);
      });
      this.store.SymptomTaskTemplate.readListPaged({
        plan_template__id: this.planTemplateId,
      }).subscribe((symptoms) => {
        this.symptomTemplates = symptoms;
      });
      this.store.InfoMessageQueue.readListPaged({
        plan_template__id: this.planTemplateId,
      }).subscribe((messages) => {
        this.messageQueues = messages;
      });
      this.store.VitalsTaskTemplate.readListPaged({
        plan_template__id: this.planTemplateId,
      }).subscribe((vitals) => {
        this.vitalTemplates = vitals;
      });
      this.store.PatientTaskTemplate.readListPaged({
        plan_template__id: this.planTemplateId,
        start_on_day: 1,
      }).subscribe((patientTasks) => {
        this.patientTaskTemplates = patientTasks;
      });
      this.store.AssessmentTaskTemplate.readListPaged({
        plan_template__id: this.planTemplateId,
      }).subscribe((assessments) => {
        this.assessmentTemplates = assessments;
      });
    });
  }

  public ngOnDestroy() { }

  public patientTasksCount() {
    return this.symptomTemplates.length + this.vitalTemplates.length + this.patientTaskTemplates.length + this.assessmentTemplates.length;
  }

  public formatStartOnDay(day) {
    if (day === 0) {
      return 'Plan Start';
    } else if (day >= 7) {
      return `Week ${day/7}`;
    } else {
      return `Day ${day}`;
    }
  }

  public formatEndOnDay(day, duration) {
    if (duration === -1) {
      return 'Until Plan Ends';
    } else {
      return `Week ${Math.round((day/7) + duration)}`;
    }
  }

  public openGoal() {
    let modalSub = this.modals.open(GoalComponent, {
      closeDisabled: true,
      data: {
        creatingTemplate: true,
      },
      width: '512px',
    }).subscribe(
      (results) => {
        if (results !== null) {
          let createSub = this.store.GoalTemplate.create({
            name: results.name,
            plan_template: this.planTemplateId,
            description: results.description,
            focus: results.focus,
            duration_weeks: results.duration_weeks,
            start_on_day: results.start_on_day,
          }).subscribe(
            (goal) => {
              this.goalTemplates.push(goal);
            },
            (err) => {},
            () => {
              createSub.unsubscribe();
            }
          );
        }
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editGoal(goal) {
    let goalIndex = this.goalTemplates.indexOf((obj) => {
      return obj.id === goal.id;
    });
    let modalSub = this.modals.open(GoalComponent, {
      closeDisabled: true,
      data: {
        creatingTemplate: false,
        goalTemplate: goal,
      },
      width: '512px',
    }).subscribe(
      (results) => {
        if (results !== null) {
          let updateSub = this.store.GoalTemplate.update(goal.id, {
            name: results.name,
            description: results.description,
            focus: results.focus,
            duration_weeks: results.duration_weeks,
            start_on_day: results.start_on_day,
          }, true).subscribe(
            (updatedGoal) => {
              this.goalTemplates[goalIndex] = updatedGoal;
            },
            (err) => {},
            () => {
              updateSub.unsubscribe();
            }
          );
        }
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
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
    }).subscribe((task) => {
      if (task !== null) {
        this.editCTTask(task);
      }
    });
  }

  public editCTTask(task) {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
      data: {
        task: task,
      },
    }).subscribe((task) => {
      let updateSub = this.store.TeamTaskTemplate.update(task.id, task, true).subscribe(
        (res) => {},
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
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
      data: {taskList: this.patientTaskTemplates, planTemplateId: this.planTemplateId, dataModel: this.store.PatientTaskTemplate},
      width: '384px',
    }).subscribe((task) => {
      if (task !== null) {
        this.editTask(task);
      }
    });
  }

  public editTask(task) {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      data: {
        task: task,
      },
      width: '384px',
    }).subscribe((task) => {
      if (task !== null) {
        let updateSub = this.store.PatientTaskTemplate.update(task.id, task, true).subscribe(
          (task) => {},
          (err) => {},
          () => {
            updateSub.unsubscribe();
          },
        );
      }
    });
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
      data: {
        editingTemplate: true,
        assessmentsList: this.assessmentTemplates,
        planTemplateId: this.planTemplateId,
      },
      width: '768px',
    }).subscribe((res) => {
      if (!res) {
        return;
      }
      if (res === 'create-new') {
        this.editAssessment(null);
      } else {
        this.editAssessment(res);
      }
    });
  }

  public editAssessment(assessment) {
    this.modals.open(CreateAssessmentComponent, {
      closeDisabled: true,
      data: {
        assessment: assessment,
        planTemplateId: this.planTemplateId,
      },
      width: '864px',
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
