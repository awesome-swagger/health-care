import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import {
  AddAssessmentComponent,
  AddCTTaskComponent,
  AddStreamComponent,
  AddVitalComponent,
  CreateAssessmentComponent,
  CreateStreamComponent,
  EditTaskComponent,
  GoalComponent,
  PreviewVitalComponent,
  CreateVitalComponent,
  PlanDurationComponent,
} from '../../../components';
import { AuthService, NavbarService, StoreService } from '../../../services';

@Component({
  selector: 'app-plan-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.scss'],
})
export class PlanScheduleComponent implements OnDestroy, OnInit {

  public planTemplateId = null;
  public planTemplate = null;
  public totalPatients = 0;
  public organization = null;
  public planTemplateAverage = null;
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

  private authSub = null;
  private routeParamsSub = null;

  constructor(
    private route: ActivatedRoute,
    private modals: ModalService,
    private auth: AuthService,
    private nav: NavbarService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.routeParamsSub = this.route.params.subscribe((params) => {
      this.planTemplateId = params.id;
      this.nav.planDetailState(this.planTemplateId);
      this.store.CarePlanTemplate.read(this.planTemplateId).subscribe((planTemplate) => {
        this.planTemplate = planTemplate;
        this.authSub = this.auth.organization$.subscribe((organization) => {
          if (!organization) {
            return;
          }
          this.organization = organization;
          this.store.CarePlanTemplate.detailRoute('get', this.planTemplate.id, 'average', {}, {
            care_plans__patient__facility__organization: this.organization.id,
          }).subscribe(
            (average) => {
              this.planTemplateAverage = average;
              this.totalPatients = this.planTemplateAverage ? this.planTemplateAverage.total_patients : 0;
            },
            (err) => {},
            () => {}
          );
        });
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

  public ngOnDestroy() {
    if (this.routeParamsSub) {
      this.routeParamsSub.unsubscribe();
    }
    if (this.authSub) {
      this.authSub.unsubscribe();
    }
  }

  public patientTasksCount() {
    return this.symptomTemplates.length + this.vitalTemplates.length + this.patientTaskTemplates.length + this.assessmentTemplates.length;
  }

  public formatStartOnDay(day) {
    if (day === 0) {
      return 'Plan Start';
    } else if (day >= 7) {
      return `Week ${Math.floor(day/7)}`;
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
      closeDisabled: false,
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
    let goalIndex = this.goalTemplates.findIndex((obj) => {
      return obj.id === goal.id;
    });
    let modalSub = this.modals.open(GoalComponent, {
      closeDisabled: false,
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

  public confirmDeleteGoal(goal) {
    let goalIndex = this.goalTemplates.findIndex((obj) => {
      return obj.id === goal.id;
    });
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Goal?',
       body: `Are you sure you want to delete this care plan goal? This will affect ${this.totalPatients} patients currently assigned to this care plan.`,
       cancelText: 'Cancel',
       okText: 'Confirm',
      },
      width: '384px',
    }).subscribe(
      (result) => {
        if (!result) return;
        if (result.toLowerCase() === 'confirm') {
          let deleteSub = this.store.GoalTemplate.destroy(goal.id).subscribe(
            (data) => {
              this.goalTemplates.splice(goalIndex, 1);
            },
            (err) => {},
            () => {
              deleteSub.unsubscribe();
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

  public addCMTask() {
    let modalSub = this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      width: '384px',
      data: {
        type: 'manager',
        planTemplateId: this.planTemplateId,
        totalPatients: this.totalPatients,
        taskList:this.teamManagerTemplates,
      },
    }).subscribe(
      (task) => {
        if (!task) {
          return;
        }
        this.editCMTask(task);
      },
      () => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editCMTask(task) {
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      width: '384px',
      data: {
        task: task,
        totalPatients: this.totalPatients,
        type: 'manager',
      },
    }).subscribe(
      (task) => {},
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public addCTTask() {
    let modalSub = this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      width: '384px',
      data: {
        type: 'team',
        planTemplateId: this.planTemplateId,
        totalPatients: this.totalPatients,
        taskList:this.teamMemberTemplates,
      },
    }).subscribe(
      (task) => {
        if (task !== null) {
          this.editCTTask(task);
        }
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editCTTask(task) {
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      width: '384px',
      data: {
        task: task,
        totalPatients: this.totalPatients,
        type: 'team',
      },
    }).subscribe(
      (task) => {},
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public confirmDeleteCTTask(task, is_manager_task) {
    let tasksIndex = this.teamTaskTemplates.findIndex((obj) => {
      return obj.id === task.id;
    });
    let otherIndex = -1;
    if (is_manager_task) {
      otherIndex = this.teamManagerTemplates.findIndex((obj) => {
        return obj.id === task.id;
      });
    } else {
      otherIndex = this.teamMemberTemplates.findIndex((obj) => {
        return obj.id === task.id;
      });
    }
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Task?',
       body: `Are you sure you want to remove this task? This will affect ${this.totalPatients} patients currently assigned to this care plan.`,
       cancelText: 'Cancel',
       okText: 'confirm',
      },
      width: '384px',
    }).subscribe(
      (data) => {
        if (!data) return;
        if (data.toLowerCase() === 'confirm') {
          let destroySub = this.store.TeamTaskTemplate.destroy(task.id).subscribe(
            (resp) => {
              this.teamTaskTemplates.splice(tasksIndex, 1);
              if (is_manager_task) {
                this.teamManagerTemplates.splice(otherIndex, 1);
              } else {
                this.teamMemberTemplates.splice(otherIndex, 1);
              }
            },
            (err) => {},
            () => {
              destroySub.unsubscribe();
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

  public addTask() {
    let modalSub = this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'patient',
        planTemplateId: this.planTemplateId,
        totalPatients: this.totalPatients,
        taskList: this.patientTaskTemplates,
      },
      width: '384px',
    }).subscribe(
      (task) => {
        if (!task) return;
        this.editTask(task);
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editTask(task) {
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        task: task,
        totalPatients: this.totalPatients,
        type: 'patient',
      },
      width: '384px',
    }).subscribe(
      (task) => {},
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public confirmDeleteTask(task) {
    let tasksIndex = this.patientTaskTemplates.findIndex((obj) => {
      return obj.id === task.id;
    });
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Task?',
       body: `Are you sure you want to remove this task? This will affect ${this.totalPatients} patients currently assigned to this care plan.`,
       cancelText: 'Cancel',
       okText: 'confirm',
      },
      width: '384px',
    }).subscribe(
      (resp) => {
        if (!resp) return;
        if (resp.toLowerCase() === 'confirm') {
          let deleteSub = this.store.PatientTaskTemplate.destroy(task.id).subscribe(
            (data) => {
              this.patientTaskTemplates.splice(tasksIndex, 1);
            },
            (err) => {},
            () => {
              deleteSub.unsubscribe();
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

  public addAssessment() {
    let modalSub = this.modals.open(AddAssessmentComponent, {
      closeDisabled: false,
      data: {
        editingTemplate: true,
        totalPatients: this.totalPatients,
        assessmentsList: this.assessmentTemplates,
        planTemplateId: this.planTemplateId,
      },
      width: '768px',
    }).subscribe(
      (res) => {
        if (!res) return;
        if (res === 'create-new') {
          setTimeout(() => {
            this.editAssessment(null);
          }, 10);
        } else {
          setTimeout(() => {
            this.editAssessment(res);
          }, 10);
        }
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editAssessment(assessment) {
    let modalSub = this.modals.open(CreateAssessmentComponent, {
      closeDisabled: false,
      data: {
        assessment: assessment,
        totalPatients: this.totalPatients,
        planTemplateId: this.planTemplateId,
      },
      width: '864px',
    }).subscribe(
      (res) => {
        if (!res) return;
        let index = this.assessmentTemplates.findIndex((obj) => {
          return obj.id === res.id;
        });
        if (index >= 0) {
          this.assessmentTemplates[index] = res;
        } else {
          this.assessmentTemplates.push(res);
        }
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editAssessmentTime(assessment) {
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        task: assessment,
        totalPatients: this.totalPatients,
        type: 'assessment',
      },
      width: '384px'
    }).subscribe(
      () => {},
      () => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public confirmDeleteAssessment(assessment) {
    let tasksIndex = this.assessmentTemplates.findIndex((obj) => {
      return obj.id === assessment.id;
    });
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Assessment?',
       body: `Are you sure you want to remove this assessment? This will affect ${this.totalPatients} patients currently assigned to this care plan.`,
       cancelText: 'Cancel',
       okText: 'Confirm',
      },
      width: '384px',
    }).subscribe(
      (data) => {
        if (!data) return;
        if (data.toLowerCase() === 'confirm') {
          let destroySub = this.store.AssessmentTaskTemplate.destroy(assessment.id).subscribe(
            (data) => {
              this.assessmentTemplates.splice(tasksIndex, 1);
            },
            (err) => {},
            () => {
              destroySub.unsubscribe();
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

  public addSymptom() {
    this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'symptom',
        task: {
          start_on_day: 0,
          appear_time: '00:00:00',
          due_time: '00:00:00',
          plan_template: this.planTemplateId,
          totalPatients: this.totalPatients,
          frequency: 'once',
        }
      },
      width: '384px',
    }).subscribe((symptom) => {
      if (!symptom) return;
      this.symptomTemplates.push(symptom);
    });
  }

  public editSymptom(symptom) {
    this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'symptom',
        totalPatients: this.totalPatients,
        task: symptom,
      },
      width: '384px',
    }).subscribe(() => {});
  }

  public confirmDeleteSymptom(symptom) {
    let tasksIndex = this.symptomTemplates.findIndex((obj) => {
      return obj.id === symptom.id;
    });
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Symptom Report?',
       body: `Are you sure you want to remove this symptom report? This will affect ${this.totalPatients} patients currently assigned to this care plan.`,
       cancelText: 'Cancel',
       okText: 'Confirm',
      },
      width: '384px',
    }).subscribe(
      (data) => {
        if (!data) return;
        if (data.toLowerCase() === 'confirm') {
          let destroySub = this.store.SymptomTaskTemplate.destroy(symptom.id).subscribe(
            (data) => {
              this.symptomTemplates.splice(tasksIndex, 1);
            },
            (err) => {},
            () => {
              destroySub.unsubscribe();
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

  public addVital(vitalTemplates) {
    this.modals.open(AddVitalComponent, {
      closeDisabled: false,
      width: '768px',
      data: {
        editingTemplate: true,
        taskList: vitalTemplates,
        totalPatients: this.totalPatients,
        planTemplateId: this.planTemplateId,
      },
    }).subscribe((data) => {
      if (!data || !data.nextAction) {
        return;
      }
      switch(data.nextAction)
      {
        case 'fullVitalPreview':
          setTimeout(() => {
            this.previewVital(data.data);
          }, 10);
          break;
        case 'editVital':
          setTimeout(() => {
            this.editVital(data.data);
          }, 10);
          break;
        default:
           break;
      }
    });
  }

  public editVital(vital) {
    this.modals.open(CreateVitalComponent, {
      closeDisabled: false,
      width: '800px',
      data: {
        vital: vital,
        planTemplateId: this.planTemplateId,
        totalPatients: this.totalPatients,
      }
    }).subscribe((res) => {
      if (!res) return;
      let index = this.vitalTemplates.findIndex((obj) => {
        return obj.id === res.id;
      });
      if (index >= 0) {
        this.vitalTemplates[index] = res;
      } else {
        this.vitalTemplates.push(res);
      }
    });
  }

  public editVitalTime(vital) {
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'vital',
        task: vital,
        totalPatients: this.totalPatients,
      },
      width: '384px',
    }).subscribe(
      (data) => {},
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public previewVital(vital) {
    this.modals.open(PreviewVitalComponent, {
      closeDisabled: false,
      width: '500px',
      data: vital
    }).subscribe(() => {});
  }

  public confirmDeleteVital(vital) {
    let tasksIndex = this.vitalTemplates.findIndex((obj) => {
      return obj.id === vital.id;
    });
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Vital?',
       body: `Are you sure you want to remove this vital report? This will affect ${this.totalPatients} patients currently assigned to this care plan.`,
       cancelText: 'Cancel',
       okText: 'Confirm',
      },
      width: '384px',
    }).subscribe(
      (data) => {
        if (!data) return;
        if (data.toLowerCase() === 'confirm') {
          let destroySub = this.store.VitalsTaskTemplate.destroy(vital.id).subscribe(
            (data) => {
              this.vitalTemplates.splice(tasksIndex, 1);
            },
            (err) => {},
            () => {
              destroySub.unsubscribe();
            }
          )
        }
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public addStream() {
    this.modals.open(AddStreamComponent, {
      closeDisabled: false,
      data: {
        editingTemplate: true,
        taskList: this.messageQueues,
        totalPatients: this.totalPatients,
        planTemplateId: this.planTemplateId,
      },
      width: '768px',
    }).subscribe((data) => {
      if (data) {
        switch (data.nextAction) {
          case 'create-stream':
            setTimeout(() => {
              this.editStream(null);
            }, 10);
        	case 'edit-stream':
            setTimeout(() => {
              this.editStream(data.message);
            }, 10);
        		break;
        	default:
        		break;
        }
      }
    });
  }

  public editStream(stream) {
    this.modals.open(CreateStreamComponent, {
      closeDisabled: false,
      data: {
        stream: stream,
        totalPatients: this.totalPatients,
        planTemplateId: this.planTemplateId,
      },
      width: '768px',
    }).subscribe((updatedStream) => {
      if (!updatedStream) return;
      let index = this.messageQueues.findIndex((obj) => {
        return obj.id === updatedStream.id;
      });
      if (index >= 0) {
        this.messageQueues[index] = updatedStream;
      } else {
        this.messageQueues.push(updatedStream);
      }
    });
  }

  public confirmDeleteStream() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Message Stream?',
       body: `Are you sure you want to remove this message stream? This will affect ${this.totalPatients} patients currently assigned to this care plan.`,
       cancelText: 'Cancel',
       okText: 'confirm',
      },
      width: '384px',
    }).subscribe(() => {});
  }
}
