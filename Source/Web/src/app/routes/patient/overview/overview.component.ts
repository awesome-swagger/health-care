import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { omit as _omit } from 'lodash';
import { ModalService, ConfirmModalComponent } from '../../../modules/modals';
import {
  GoalComponent,
  AddCTTaskComponent,
  AddVitalComponent,
  AddAssessmentComponent,
  AddStreamComponent,
  EditTaskComponent,
  CreateStreamComponent,
  CreateAssessmentComponent,
  CreateVitalComponent,
  PreviewVitalComponent,
} from '../../../components';
import { AuthService, NavbarService, StoreService, TimeTrackerService, } from '../../../services';
import { MedicationComponent } from '../modals/medication/medication.component';

@Component({
  selector: 'app-patient-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss'],
})
export class PatientOverviewComponent implements OnDestroy, OnInit {

  public user = null;
  public patient = null;
  public carePlan = null;
  public planGoals = [];
  public planTeamTasks = [];
  public planTeamManagerTasks = [];
  public planTeamMemberTasks = [];
  public planPatientTasks = [];
  public planAssessmentTasks = [];
  public planSymptomTasks = [];
  public planVitalTasks = [];
  public planMedicationTasks = [];
  public planCareMessages = [];

  public tooltipsOpen = {};
  public accordionsOpen = {};

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private auth: AuthService,
    private nav: NavbarService,
    private store: StoreService,
    private timer: TimeTrackerService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.patientId, params.planId);
      this.auth.user$.subscribe((user) => {
    		if (!user) {
    			return;
    		}
        this.user = user;
        this.store.PatientProfile.read(params.patientId).subscribe(
          (patient) => {
            this.patient = patient;
            this.nav.addRecentPatient(this.patient);
            this.store.CarePlan.read(params.planId).subscribe(
              (carePlan) => {
                this.carePlan = carePlan;
                this.timer.startTimer(this.user, this.carePlan);
                this.fetchPlanSchedule(this.carePlan);
              }
            );
          },
          (err) => {},
          () => {},
        );
      });
    });
  }

  public ngOnDestroy() {
    this.timer.stopTimer();
  }

  public fetchPlanGoals(planTemplateId) {
    let promise = new Promise((resolve, reject) => {
      let goalsSub = this.store.GoalTemplate.readListPaged({
        plan_template__id: planTemplateId,
        is_active: true,
      }).subscribe(
        (goals) => resolve(goals),
        (err) => reject(err),
        () => {
          goalsSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public fetchTeamTasks(planId) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.PlanTeamTemplate.readListPaged({
        plan: planId
      }).subscribe(
        (teamTasks) => resolve(teamTasks),
        (err) => reject(err),
        () => {
          tasksSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public fetchPatientTasks(planId) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.PlanPatientTemplate.readListPaged({
        plan: planId
      }).subscribe(
        (patientTasks) => resolve(patientTasks),
        (err) => reject(err),
        () => {
          tasksSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public fetchAssessments(planTemplateId) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.AssessmentTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
        is_active: true,
      }).subscribe(
        (assessmentTasks) => resolve(assessmentTasks),
        (err) => reject(err),
        () => {
          tasksSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public fetchSymptomTasks(planId) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.PlanSymptomTemplate.readListPaged({
        plan: planId,
      }).subscribe(
        (symptomTasks) => resolve(symptomTasks),
        (err) => reject(err),
        () => {
          tasksSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public fetchVitalTasks(planTemplateId) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.VitalsTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
        is_active: true,
      }).subscribe(
        (vitalTasks) => resolve(vitalTasks),
        (err) => reject(err),
        () => {
          tasksSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public fetchMedicationTasks(planId) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.MedicationTaskTemplate.readListPaged({
        plan__id: planId,
        is_active: true,
      }).subscribe(
        (medicationTasks) => resolve(medicationTasks),
        (err) => reject(err),
        () => {
          tasksSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public fetchCareMessages(planTemplateId) {
    let promise = new Promise((resolve, reject) => {
      let messagesSub = this.store.InfoMessageQueue.readListPaged({
        plan_template__id: planTemplateId,
        is_active: true,
      }).subscribe(
        (careMessages) => resolve(careMessages),
        (err) => reject(err),
        () => {
          messagesSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public fetchPlanSchedule(carePlan) {
    this.fetchPlanGoals(carePlan.plan_template.id).then((planGoals: any) => {
      this.planGoals = planGoals;
    });
    this.fetchTeamTasks(carePlan.id).then((planTeamTasks: any) => {
      this.planTeamTasks = planTeamTasks;
      this.planTeamManagerTasks = planTeamTasks.filter((task) => task.team_task_template.is_manager_task);
      this.planTeamMemberTasks = planTeamTasks.filter((task) => !task.team_task_template.is_manager_task);
    });
    this.fetchPatientTasks(carePlan.id).then((planPatientTasks: any) => {
      this.planPatientTasks = planPatientTasks;
    });
    this.fetchAssessments(carePlan.plan_template.id).then((planAssessmentTasks: any) => {
      this.planAssessmentTasks = planAssessmentTasks;
    });
    this.fetchSymptomTasks(carePlan.id).then((planSymptomTasks: any) => {
      this.planSymptomTasks = planSymptomTasks;
    });
    this.fetchVitalTasks(carePlan.plan_template.id).then((planVitalTasks: any) => {
      this.planVitalTasks = planVitalTasks;
    });
    this.fetchMedicationTasks(carePlan.id).then((planMedicationTasks: any) => {
      this.planMedicationTasks = planMedicationTasks;
    });
    this.fetchCareMessages(carePlan.plan_template.id).then((planCareMessages: any) => {
      this.planCareMessages = planCareMessages;
    });
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

  public patientTasksCount() {
    return this.planSymptomTasks.length + this.planVitalTasks.length + this.planPatientTasks.length + this.planAssessmentTasks.length;
  }

  public openGoal() {
    this.modals.open(GoalComponent, {
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
            plan_template: this.carePlan.plan_template.id,
            description: results.description,
            focus: results.focus,
            duration_weeks: results.duration_weeks,
            start_on_day: results.start_on_day,
          }).subscribe(
            (goal) => {
              this.planGoals.push(goal);
            },
            (err) => {},
            () => {
              createSub.unsubscribe();
            }
          );
        }
      }
    );
  }

  public editGoal(goal) {
    let goalIndex = this.planGoals.findIndex((obj) => {
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
              this.planGoals[goalIndex] = updatedGoal;
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
    let goalIndex = this.planGoals.findIndex((obj) => {
      return obj.id === goal.id;
    });
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Goal?',
       body: `Are you sure you want to delete this care plan goal?`,
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
              this.planGoals.splice(goalIndex, 1);
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
        type: 'plan-manager',
        planId: this.carePlan.id,
      },
      width: '384px',
    }).subscribe(
      (newTask) => {
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
    let taskIndex = this.planTeamManagerTasks.findIndex((obj) => obj.id === task.id);
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'plan-manager',
        task: task,
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (updatedTask) => {
        this.fetchTeamTasks(this.carePlan.id).then((planTeamTasks: any) => {
          this.planTeamTasks = planTeamTasks;
          this.planTeamManagerTasks = planTeamTasks.filter((task) => task.team_task_template.is_manager_task);
          this.planTeamMemberTasks = planTeamTasks.filter((task) => !task.team_task_template.is_manager_task);
        });
        if (!updatedTask) return;
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public formatSelectedRoles(task) {
    if (!task.team_task_template.roles || task.team_task_template.roles.length < 1) {
      return '';
    }
    if (task.team_task_template.roles.length > 1) {
      return `${task.team_task_template.roles[0].name}, +${task.team_task_template.roles.length - 1}`
    } else {
      return task.team_task_template.roles[0].name;
    }
  }

  public addTeamTask() {
    let modalSub = this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'plan-team',
        planId: this.carePlan.id,
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (newTask) => {
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
    let taskIndex = this.planTeamMemberTasks.findIndex((obj) => obj.id === task.id);
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'plan-team',
        task: task,
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (updatedTask) => {
        this.fetchTeamTasks(this.carePlan.id).then((planTeamTasks: any) => {
          this.planTeamTasks = planTeamTasks;
          this.planTeamManagerTasks = planTeamTasks.filter((task) => task.team_task_template.is_manager_task);
          this.planTeamMemberTasks = planTeamTasks.filter((task) => !task.team_task_template.is_manager_task);
        });
        if (!updatedTask) return;
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public deleteTeamTask(task, is_manager_task) {
    let tasksIndex = this.planTeamTasks.findIndex((obj) => {
      return obj.id === task.id;
    });
    let otherIndex = -1;
    if (is_manager_task) {
      otherIndex = this.planTeamManagerTasks.findIndex((obj) => {
        return obj.id === task.id;
      });
    } else {
      otherIndex = this.planTeamMemberTasks.findIndex((obj) => {
        return obj.id === task.id;
      });
    }
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Task?',
       body: `Are you sure you want to remove this task from this patient's care plan?`,
       cancelText: 'Cancel',
       okText: 'confirm',
      },
      width: '384px',
    }).subscribe(
      (data) => {
        if (!data) return;
        if (data.toLowerCase() === 'confirm') {
          let destroySub = this.store.PlanTeamTemplate.destroy(task.id).subscribe(
            (resp) => {
              this.planTeamTasks.splice(tasksIndex, 1);
              if (is_manager_task) {
                this.planTeamManagerTasks.splice(otherIndex, 1);
              } else {
                this.planTeamMemberTasks.splice(otherIndex, 1);
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
        type: 'plan-patient',
        planId: this.carePlan.id,
      },
      width: '384px',
    }).subscribe(
      (newTask) => {
        console.log(newTask);
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
    let taskIndex = this.planPatientTasks.findIndex((obj) => obj.id === task.id);
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'plan-patient',
        task: task,
        totalPatients: 0,
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe(
      (updatedTask) => {
        this.fetchPatientTasks(this.carePlan.id).then((planPatientTasks: any) => {
          this.planPatientTasks = planPatientTasks;
        });
        if (!updatedTask) return;
      },
      (err) => {},
      () => {
        modalSub.unsubscribe();
      }
    );
  }

  public deletePatientTask(task) {
    let tasksIndex = this.planPatientTasks.findIndex((obj) => {
      return obj.id === task.id;
    });
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Task?',
       body: `Are you sure you want to remove this task from this patient's care plan?`,
       cancelText: 'Cancel',
       okText: 'confirm',
      },
      width: '384px',
    }).subscribe(
      (resp) => {
        if (!resp) return;
        if (resp.toLowerCase() === 'confirm') {
          let deleteSub = this.store.PlanPatientTemplate.destroy(task.id).subscribe(
            (data) => {
              this.planPatientTasks.splice(tasksIndex, 1);
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
        totalPatients: 0,
        planTemplateId: this.carePlan.plan_template.id,
      },
      width: '768px',
    }).subscribe(
      (res) => {
        this.fetchAssessments(this.carePlan.plan_template.id).then((assessments: any) => {
          this.planAssessmentTasks = assessments;
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
        totalPatients: 0,
        planTemplateId: this.carePlan.plan_template.id,
      },
      width: '864px',
    }).subscribe(
      (res) => {
        if (!res) return;
        let index = this.planAssessmentTasks.findIndex((obj) => {
          return obj.id === res.id;
        });
        if (index >= 0) {
          this.planAssessmentTasks[index] = res;
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
        totalPatients: 0,
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
    let tasksIndex = this.planAssessmentTasks.findIndex((obj) => {
      return obj.id === assessment.id;
    });
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Assessment?',
       body: `Are you sure you want to remove this assessment from this patient's care plan?`,
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
              this.planAssessmentTasks.splice(tasksIndex, 1);
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
        type: 'plan-symptom',
        planId: this.carePlan.id,
        totalPatients: 0,
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe((symptom) => {
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
        type: 'plan-symptom',
        task: symptom,
        totalPatients: 0,
      },
      overflow: 'visible',
      width: '384px',
    }).subscribe((res) => {
      this.fetchSymptomTasks(this.carePlan.id).then((planSymptomTasks: any) => {
        this.planSymptomTasks = planSymptomTasks;
      });
      if (!res) return;
    });
  }

  public deleteSymptom(symptom) {
    let tasksIndex = this.planSymptomTasks.findIndex((obj) => {
      return obj.id === symptom.id;
    });
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Symptom Report?',
       body: `Are you sure you want to remove this symptom report from this patient's care plan?`,
       cancelText: 'Cancel',
       okText: 'Confirm',
      },
      width: '384px',
    }).subscribe(
      (data) => {
        if (!data) return;
        if (data.toLowerCase() === 'confirm') {
          let destroySub = this.store.PlanSymptomTemplate.destroy(symptom.id).subscribe(
            (data) => {
              this.planSymptomTasks.splice(tasksIndex, 1);
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

  public addVital() {
    this.modals.open(AddVitalComponent, {
      closeDisabled: false,
      width: '768px',
      data: {
        editingTemplate: true,
        totalPatients: 0,
        planTemplateId: this.carePlan.plan_template.id,
      },
    }).subscribe((data) => {
      this.fetchVitalTasks(this.carePlan.plan_template.id).then((planVitalTasks: any) => {
        this.planVitalTasks = planVitalTasks;
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
        planTemplateId: this.carePlan.plan_template.id,
        totalPatients: 0,
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
      let index = this.planVitalTasks.findIndex((obj) => {
        return obj.id === res.id;
      });
      if (index >= 0) {
        this.planVitalTasks[index] = res;
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
        totalPatients: 0,
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
          this.addVital();
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
    let tasksIndex = this.planVitalTasks.findIndex((obj) => {
      return obj.id === vital.id;
    });
    let modalSub = this.modals.open(ConfirmModalComponent, {
     closeDisabled: true,
     data: {
       title: 'Delete Vital?',
       body: `Are you sure you want to remove this vital report from this patient's care plan?`,
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
              this.planVitalTasks.splice(tasksIndex, 1);
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

  public addMedication() {
    this.modals.open(MedicationComponent, {
      closeDisabled: false,
      data: {
        type: 'add',
        patient: this.patient,
        plans: [this.carePlan],
      },
      width: '540px',
    }).subscribe((data) => {
      this.fetchMedicationTasks(this.carePlan.id).then((planMedicationTasks: any) => {
        this.planMedicationTasks = planMedicationTasks;
      });
    });
  }

  public editMedication(medication) {
    let patientMedication = Object.assign({}, medication.patient_medication);
    let excludePatientMedication = _omit(Object.assign({}, medication), 'patient_medication');
    let modalMedicationData = Object.assign({}, patientMedication, {task: excludePatientMedication});
    this.modals.open(MedicationComponent, {
      width: '576px',
      data: {
        type: 'edit',
        patient: this.patient,
        plans: [this.carePlan],
        medication: modalMedicationData,
      }
    }).subscribe((res) => {
      this.fetchMedicationTasks(this.carePlan.id).then((planMedicationTasks: any) => {
        this.planMedicationTasks = planMedicationTasks;
      });
    });
  }

  public confirmDeleteMedication() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Task?',
       body: 'Are you sure you want to remove this medication task from this patient\'s care plan?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public addStream() {
    this.modals.open(AddStreamComponent, {
      closeDisabled: false,
      data: {
        editingTemplate: true,
        totalPatients: 0,
        planTemplateId: this.carePlan.plan_template.id,
      },
      width: '768px',
    }).subscribe((data) => {
      this.fetchCareMessages(this.carePlan.plan_template.id).then((planCareMessages: any) => {
        this.planCareMessages = planCareMessages;
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
        totalPatients: 0,
        planTemplateId: this.carePlan.plan_template.id,
      },
      width: '768px',
    }).subscribe((updatedStream) => {
      if (!updatedStream) return;
      let index = this.planCareMessages.findIndex((obj) => {
        return obj.id === updatedStream.id;
      });
      if (index >= 0) {
        this.planCareMessages[index] = updatedStream;
      } else {
        this.planCareMessages.push(updatedStream);
      }
    });
  }

  public deleteStream(stream) {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Care Message?',
       body: `Are you sure you want to remove this care message from this patient's care plan?`,
       cancelText: 'Cancel',
       okText: 'Confirm',
      },
      width: '384px',
    }).subscribe((res) => {
      if (!res) return;
      if (res.toLowerCase() === 'confirm') {
        let messagesIndex = this.planCareMessages.findIndex((obj) => {
          return obj.id === stream.id;
        });
        let destroySub = this.store.InfoMessageQueue.update(stream.id, {
          is_active: false,
        }, true).subscribe(
          (data) => {
            this.planCareMessages.splice(messagesIndex, 1);
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
