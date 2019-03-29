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
          this.getPlanTemplateAverage(this.planTemplate.id, this.organization.id).then((average: any) => {
            this.planTemplateAverage = average;
            this.totalPatients = this.planTemplateAverage ? this.planTemplateAverage.total_patients : 0;
          });
          this.getPlanTemplateSchedule(this.planTemplate.id);
        });
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

  public getPlanTemplateAverage(planTemplateId, organizationId) {
    let promise = new Promise((resolve, reject) => {
      let averageSub = this.store.CarePlanTemplate.detailRoute('get', planTemplateId, 'average', {}, {
        care_plans__patient__facility__organization: organizationId,
      }).subscribe(
        (average) => resolve(average),
        (err) => reject(err),
        () => averageSub.unsubscribe()
      );
    });
    return promise;
  }

  public getGoals(planTemplateId) {
    return new Promise((resolve, reject) => {
      let goalsSub = this.store.GoalTemplate.readListPaged({
        plan_template__id: planTemplateId,
      }).subscribe(
        (goals) => resolve(goals),
        (err) => reject(err),
        () => goalsSub.unsubscribe()
      );
    });
  }

  public getTeamTasks(planTemplateId) {
    return new Promise((resolve, reject) => {
      let teamTasksSub = this.store.TeamTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
        is_active: true,
      }).subscribe(
        (teamTaskTemplates) => resolve(teamTaskTemplates),
        (err) => reject(err),
        () => teamTasksSub.unsubscribe()
      );
    });
  }

  public getPatientTasks(planTemplateId) {
    return new Promise((resolve, reject) => {
      let patientTasksSub = this.store.PatientTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
        is_active: true,
      }).subscribe(
        (patientTasks) => resolve(patientTasks),
        (err) => reject(err),
        () => patientTasksSub.unsubscribe()
      );
    });
  }

  public getAssessmentTasks(planTemplateId) {
    return new Promise((resolve, reject) => {
      let assessmentTasksSub = this.store.AssessmentTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
        is_active: true,
      }).subscribe(
        (assessments) => resolve(assessments),
        (err) => reject(err),
        () => assessmentTasksSub.unsubscribe()
      );
    });
  }

  public getSymptomTasks(planTemplateId) {
    return new Promise((resolve, reject) => {
      let symptomTasksSub = this.store.SymptomTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
        is_active: true,
      }).subscribe(
        (symptoms) => resolve(symptoms),
        (err) => reject(err),
        () => symptomTasksSub.unsubscribe()
      );
    });
  }

  public getVitalTasks(planTemplateId) {
    return new Promise((resolve, reject) => {
      let vitalTasksSub = this.store.VitalsTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
        is_active: true,
      }).subscribe(
        (vitals) => resolve(vitals),
        (err) => reject(err),
        () => vitalTasksSub.unsubscribe()
      );
    });
  }

  public getMessageQueues(planTemplateId) {
    return new Promise((resolve, reject) => {
      let messageQueuesSub = this.store.InfoMessageQueue.readListPaged({
        plan_template__id: planTemplateId,
        is_active: true,
      }).subscribe(
        (messages) => resolve(messages),
        (err) => reject(err),
        () => messageQueuesSub.unsubscribe()
      );
    });
  }

  public getPlanTemplateSchedule(planTemplateId) {
    this.getGoals(planTemplateId).then((goals: any) => {
      this.goalTemplates = goals;
    });
    this.getTeamTasks(planTemplateId).then((teamTaskTemplates: any) => {
      this.teamTaskTemplates = teamTaskTemplates;
      this.teamManagerTemplates = teamTaskTemplates.filter((task) => task.is_manager_task);
      this.teamMemberTemplates = teamTaskTemplates.filter((task) => !task.is_manager_task);
    });
    this.getPatientTasks(planTemplateId).then((patientTasks: any) => {
      this.patientTaskTemplates = patientTasks;
    });
    this.getAssessmentTasks(planTemplateId).then((assessments: any) => {
      this.assessmentTemplates = assessments;
    });
    this.getSymptomTasks(planTemplateId).then((symptoms: any) => {
      this.symptomTemplates = symptoms;
    });
    this.getVitalTasks(planTemplateId).then((vitals: any) => {
      this.vitalTemplates = vitals;
    });
    this.getMessageQueues(planTemplateId).then((messages: any) => {
      this.messageQueues = messages;
    });
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

  public deleteGoal(goal) {
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

  public addManagerTask() {
    let modalSub = this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'manager',
        planTemplateId: this.planTemplateId,
        totalPatients: this.totalPatients,
      },
      width: '384px',
    }).subscribe(
      (newTask) => {
        // Refetch team tasks since they might have changed in the add modal
        this.getTeamTasks(this.planTemplateId).then((teamTaskTemplates: any) => {
          this.teamTaskTemplates = teamTaskTemplates;
          this.teamManagerTemplates = teamTaskTemplates.filter((task) => task.is_manager_task);
          this.teamMemberTemplates = teamTaskTemplates.filter((task) => !task.is_manager_task);
        });
        // If a new task has been created, open the edit modal
        if (!newTask) return;
        setTimeout(() => {
          this.editManagerTask(newTask);
        }, 10);
      },
      () => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editManagerTask(task) {
    let taskIndex = this.teamManagerTemplates.findIndex((obj) => obj.id === task.id);
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        task: task,
        totalPatients: this.totalPatients,
        type: 'manager',
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (updatedTask) => {
        if (!updatedTask) return;
        this.teamManagerTemplates[taskIndex] = updatedTask;
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public addTeamTask() {
    let modalSub = this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'team',
        planTemplateId: this.planTemplateId,
        totalPatients: this.totalPatients,
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (newTask) => {
        // Refetch team tasks since they might have changed in the add modal
        this.getTeamTasks(this.planTemplateId).then((teamTaskTemplates: any) => {
          this.teamTaskTemplates = teamTaskTemplates;
          this.teamManagerTemplates = teamTaskTemplates.filter((task) => task.is_manager_task);
          this.teamMemberTemplates = teamTaskTemplates.filter((task) => !task.is_manager_task);
        });
        // If a new task has been created, open the edit modal
        if (!newTask) return;
        setTimeout(() => {
          this.editTeamTask(newTask);
        }, 10);
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editTeamTask(task) {
    let taskIndex = this.teamMemberTemplates.findIndex((obj) => obj.id === task.id);
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        task: task,
        totalPatients: this.totalPatients,
        type: 'team',
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (updatedTask) => {
        if (!updatedTask) return;
        this.teamMemberTemplates[taskIndex] = updatedTask;
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public deleteTeamTask(task, is_manager_task) {
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
          let destroySub = this.store.TeamTaskTemplate.update(task.id, {
            is_active: false,
          }, true).subscribe(
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

  public addPatientTask() {
    let modalSub = this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'patient',
        planTemplateId: this.planTemplateId,
        totalPatients: this.totalPatients,
      },
      width: '384px',
    }).subscribe(
      (newTask) => {
        this.getPatientTasks(this.planTemplateId).then((patientTasks: any) => {
          this.patientTaskTemplates = patientTasks;
        });
        if (!newTask) return;
        setTimeout(() => {
          this.editPatientTask(newTask);
        }, 10);
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editPatientTask(task) {
    let taskIndex = this.patientTaskTemplates.findIndex((obj) => obj.id === task.id);
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        task: task,
        totalPatients: this.totalPatients,
        type: 'patient',
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (updatedTask) => {
        if (!updatedTask) return;
        this.patientTaskTemplates[taskIndex] = updatedTask;
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public deletePatientTask(task) {
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
          let deleteSub = this.store.PatientTaskTemplate.update(task.id, {
            is_active: false,
          }, true).subscribe(
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
        planTemplateId: this.planTemplateId,
      },
      width: '768px',
    }).subscribe(
      (res) => {
        this.getAssessmentTasks(this.planTemplateId).then((assessments: any) => {
          this.assessmentTemplates = assessments;
        });
        if (!res) return;
        setTimeout(() => {
          this.editAssessment(res, false);
        }, 10);
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public editAssessment(assessment, isEditing) {
    let modalSub = this.modals.open(CreateAssessmentComponent, {
      closeDisabled: false,
      data: {
        assessment: assessment,
        isEditing: isEditing,
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
        }
        setTimeout(() => {
          this.editAssessmentTime(res);
        }, 10);
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
      overflow: 'visible',
      width: '384px'
    }).subscribe(
      () => {},
      () => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public deleteAssessment(assessment) {
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
          let destroySub = this.store.AssessmentTaskTemplate.update(assessment.id, {
            is_active: false,
          }, true).subscribe(
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
    this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'symptom',
        editingTemplate: true,
        totalPatients: this.totalPatients,
        planTemplateId: this.planTemplateId,
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe((symptom) => {
      this.getSymptomTasks(this.planTemplateId).then((symptoms: any) => {
        this.symptomTemplates = symptoms;
      });
      if (!symptom) return;
      setTimeout(() => {
        this.editSymptom(symptom);
      }, 10);
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
      overflow: 'visible',
      width: '384px',
    }).subscribe((res) => {
      if (!res) return;
      let index = this.symptomTemplates.findIndex((obj) => {
        return obj.id === res.id;
      });
      if (index >= 0) {
        this.symptomTemplates[index] = res;
      }
    });
  }

  public deleteSymptom(symptom) {
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
          let destroySub = this.store.SymptomTaskTemplate.update(symptom.id, {
            is_active: false,
          }, true).subscribe(
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
        totalPatients: this.totalPatients,
        planTemplateId: this.planTemplateId,
      },
    }).subscribe((data) => {
      this.getVitalTasks(this.planTemplateId).then((vitals: any) => {
        this.vitalTemplates = vitals;
      });
      if (!data || !data.nextAction) {
        return;
      }
      switch(data.nextAction)
      {
        case 'fullVitalPreview':
          setTimeout(() => {
            this.previewVital('add-vital', data.data);
          }, 10);
          break;
        case 'createVital':
          setTimeout(() => {
            this.editVital(data.data, false);
          }, 10);
        default:
           break;
      }
    });
  }

  public editVital(vital, isEditing) {
    this.modals.open(CreateVitalComponent, {
      closeDisabled: false,
      data: {
        vital: vital,
        isEditing: isEditing,
        planTemplateId: this.planTemplateId,
        totalPatients: this.totalPatients,
      },
      overflow: 'visible',
      width: '800px',
    }).subscribe((res) => {
      if (!res) return;
      if (res.next && res.next === 'preview') {
        setTimeout(() => {
          this.previewVital('edit-vital', res.vital);
        }, 10);
        return;
      }
      let index = this.vitalTemplates.findIndex((obj) => {
        return obj.id === res.id;
      });
      if (index >= 0) {
        this.vitalTemplates[index] = res;
      }
      setTimeout(() => {
        this.editVitalTime(res);
      }, 10);
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
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (data) => {},
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public previewVital(from, vital) {
    this.modals.open(PreviewVitalComponent, {
      closeDisabled: false,
      width: '384px',
      data: {
        from: from,
        vital: vital,
      }
    }).subscribe((res) => {
      if (!res) return;
      if (res.next === 'add-vital') {
        setTimeout(() => {
          this.addVital(this.vitalTemplates);
        }, 10);
      }
      if (res.next === 'edit-vital') {
        setTimeout(() => {
          this.editVital(res.vital, true);
        }, 10);
      }
    });
  }

  public deleteVital(vital) {
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
          let destroySub = this.store.VitalsTaskTemplate.update(vital.id, {
            is_active: false,
          }, true).subscribe(
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
        totalPatients: this.totalPatients,
        planTemplateId: this.planTemplateId,
      },
      width: '768px',
    }).subscribe((data) => {
      this.getMessageQueues(this.planTemplateId).then((messages: any) => {
        this.messageQueues = messages;
      });
      if (data) {
        switch (data.nextAction) {
          case 'create-stream':
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
        editingTemplate: true,
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

  public deleteStream(stream) {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Care Message?',
       body: `Are you sure you want to remove this message stream? This will affect ${this.totalPatients} patients currently assigned to this care plan.`,
       cancelText: 'Cancel',
       okText: 'Confirm',
      },
      width: '384px',
    }).subscribe((res) => {
      if (!res) return;
      if (res.toLowerCase() === 'confirm') {
        let messagesIndex = this.messageQueues.findIndex((obj) => {
          return obj.id === stream.id;
        });
        let destroySub = this.store.InfoMessageQueue.update(stream.id, {
          is_active: false,
        }, true).subscribe(
          (data) => {
            this.messageQueues.splice(messagesIndex, 1);
          },
          (err) => {},
          () => {
            destroySub.unsubscribe();
          }
        )
      }
    });
  }
}
