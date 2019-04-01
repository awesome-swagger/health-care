import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
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
} from '../../../components';
import { StoreService, NavbarService, } from '../../../services';
import { MedicationComponent } from '../modals/medication/medication.component';

@Component({
  selector: 'app-patient-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss'],
})
export class PatientOverviewComponent implements OnDestroy, OnInit {

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

  public accordCPGOpen;
  public toolCPGOpen;
  public accordCTOpen;
  public toolCTTOpen;
  public toolCMTOpen;
  public accordPTOpen;
  public toolPTTOpen;
  public toolPTAOpen;
  public toolPTA2Open;
  public toolPTA3Open;
  public toolPTSOpen;
  public toolPTVOpen;
  public toolPTMOpen;
  public toolPTMSOpen;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.patientId, params.planId);
      this.store.PatientProfile.read(params.patientId).subscribe(
        (patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
          this.store.CarePlan.read(params.planId).subscribe(
            (carePlan) => {
              this.carePlan = carePlan;
              this.fetchPlanGoals(carePlan.plan_template.id).then((planGoals: any) => {
                this.planGoals = planGoals;
              });
              this.fetchTeamTasks(carePlan.plan_template.id).then((planTeamTasks: any) => {
                this.planTeamTasks = planTeamTasks;
                this.planTeamManagerTasks = planTeamTasks.filter((task) => task.is_manager_task);
                this.planTeamMemberTasks = planTeamTasks.filter((task) => !task.is_manager_task);
              });
              this.fetchPatientTasks(carePlan.plan_template.id).then((planPatientTasks: any) => {
                this.planPatientTasks = planPatientTasks;
              });
              this.fetchAssessments(carePlan.plan_template.id).then((planAssessmentTasks: any) => {
                this.planAssessmentTasks = planAssessmentTasks;
              });
              this.fetchSymptomTasks(carePlan.plan_template.id).then((planSymptomTasks: any) => {
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
          );
        },
        (err) => {},
        () => {},
      );
    });
  }

  public patientTasksCount() {
    return this.planSymptomTasks.length + this.planVitalTasks.length + this.planPatientTasks.length + this.planAssessmentTasks.length + this.planMedicationTasks.length;
  }

  public ngOnDestroy() { }

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

  public fetchPlanGoals(planTemplateId) {
    let promise = new Promise((resolve, reject) => {
      let goalsSub = this.store.GoalTemplate.readListPaged({
        plan_template__id: planTemplateId,
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

  public fetchTeamTasks(planTemplateId) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.TeamTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
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

  public fetchPatientTasks(planTemplateId) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.PatientTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
      }).subscribe(
        (patientTasks) => resolve(patientTasks),
        (err) => reject(err),
        () => {
          tasksSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public fetchAssessments(planTemplateId) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.AssessmentTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
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

  public fetchSymptomTasks(planTemplateId) {
    let promise = new Promise((resolve, reject) => {
      let tasksSub = this.store.SymptomTaskTemplate.readListPaged({
        plan_template__id: planTemplateId,
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

  public openGoal() {
    this.modals.open(GoalComponent, {
      closeDisabled: false,
      data: {
        goalTemplate: 'test',
      },
      width: '512px',
    }).subscribe(() => {});
  }

  public editGoal(goal) {
    this.modals.open(GoalComponent, {
      closeDisabled: false,
      data: {
        creatingTemplate: false,
        goalTemplate: goal,
      },
      width: '512px',
    }).subscribe(() => {});
  }

  public confirmDeleteGoal() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Goal?',
       body: 'Are you sure you want to delete this care plan goal?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public addCMTask() {
    let modalSub = this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      width: '384px',
      data: {
        type: 'manager',
        planTemplateId: this.carePlan.plan_template.id,
        taskList: this.planTeamManagerTasks,
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
        planTemplateId: this.carePlan.plan_template.id,
        taskList: this.planTeamMemberTasks,
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

  public confirmDeleteCTTask(task) {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Task?',
       body: 'Are you sure you want to remove this task?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public addTask() {
    let modalSub = this.modals.open(AddCTTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'patient',
        planTemplateId: this.carePlan.plan_template.id,
        taskList: this.planPatientTasks,
      },
      width: '384px',
    }).subscribe(
      (task) => {
        if (!task) {
          return;
        }
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

  public confirmDeleteTask() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Task?',
       body: 'Are you sure you want to remove this task?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public addAssessment() {
    let modalSub = this.modals.open(AddAssessmentComponent, {
      closeDisabled: false,
      data: {
        editingTemplate: true,
        assessmentsList: this.planAssessmentTasks,
        planTemplateId: this.carePlan.plan_template.id,
      },
      width: '768px',
    }).subscribe(
      (res) => {
        if (!res) {
          return;
        }
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
        planTemplateId: this.carePlan.plan_template.id,
      },
      width: '864px',
    }).subscribe(
      (res) => {
        if (!res) {
          return;
        }
        let index = this.planAssessmentTasks.findIndex((obj) => {
          return obj.id === res.id;
        });
        if (index >= 0) {
          this.planAssessmentTasks[index] = res;
        } else {
          this.planAssessmentTasks.push(res);
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

  public confirmDeleteAssessment() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Assessment?',
       body: 'Are you sure you want to remove this assessment?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
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
          plan_template: this.carePlan.plan_template.id,
          frequency: 'once',
        }
      },
      width: '384px',
    }).subscribe((symptom) => {
      if (!symptom) {
        return;
      }
      this.planSymptomTasks.push(symptom);
    });
  }

  public editSymptom(symptom) {
    this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'symptom',
        task: symptom,
      },
      width: '384px',
    }).subscribe(() => {});
  }

  public confirmDeleteSymptom() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Symptom Report?',
       body: 'Are you sure you want to remove this symptom report?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public addVital() {
    this.modals.open(AddVitalComponent, {
      closeDisabled: false,
      width: '768px',
      data: {
        taskList: this.planVitalTasks,
        planTemplateId: this.carePlan.plan_template.id,
      },
    }).subscribe((data) => {
      if (!data || !data.nextAction) {
        return;
      }
      switch(data.nextAction)
      {
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
        planTemplateId: this.carePlan.plan_template.id,
      }
    }).subscribe((res) => {
      if (!res) {
        return;
      }
      let index = this.planVitalTasks.findIndex((obj) => {
        return obj.id === res.id;
      });
      if (index >= 0) {
        this.planVitalTasks[index] = res;
      } else {
        this.planVitalTasks.push(res);
      }
    });
  }

  public editVitalTime(vital) {
    let modalSub = this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'vital',
        task: vital,
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

  public confirmDeleteVital() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Vital?',
       body: 'Are you sure you want to remove this vital report?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }

  public addMedication() {
    this.modals.open(MedicationComponent, {
      closeDisabled: false,
      data: {
        plan: this.carePlan,
      },
      width: '540px',
    }).subscribe((data) => {
      if (data.patient_medication && data.task) {
        this.store.PatientMedication.create(data.patient_medication).subscribe(
          (patientMedication) => {
            data.task.patient_medication = patientMedication.id;
            this.store.MedicationTaskTemplate.create(data.task).subscribe(
              (medicationTask) => {
                this.planMedicationTasks.push(medicationTask);
              },
              (err) => {
                console.log('Error creating medication task template', err);
              },
              () => {}
            );
          },
          (err) => {
            console.log('Error creating patient medication', err);
          },
          () => {}
        );
      }
    });
  }

  public editMedication(medication) {
    this.modals.open(EditTaskComponent, {
      closeDisabled: false,
      data: {
        type: 'medication',
        task: medication,
      },
      width: '540px',
    }).subscribe((res) => {});
  }

  public confirmDeleteMedication() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Task?',
       body: 'Are you sure you want to remove this medication task?',
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
          taskList: this.planCareMessages,
          planTemplateId: this.carePlan.plan_template.id,
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
        planTemplateId: this.carePlan.plan_template.id,
      },
      width: '768px',
    }).subscribe((updatedStream) => {
      if (!updatedStream) {
        return;
      }
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

  public confirmDeleteStream() {
    this.modals.open(ConfirmModalComponent, {
     closeDisabled: false,
     data: {
       title: 'Delete Message Stream?',
       body: 'Are you sure you want to remove this message stream?',
       cancelText: 'Cancel',
       okText: 'Continue',
      },
      width: '384px',
    }).subscribe(() => {
    // do something with result
    });
  }
}
