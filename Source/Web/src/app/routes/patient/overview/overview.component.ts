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
  CreateStreamComponent
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

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  public ngOnInit() {
    this.route.params.subscribe((params) => {
      this.nav.patientDetailState(params.id);
      this.store.PatientProfile.read(params.id).subscribe(
        (patient) => {
          this.patient = patient;
          this.nav.addRecentPatient(this.patient);
        },
        (err) => {},
        () => {},
      );
    });
  }

  public ngOnDestroy() { }

  public openGoal() {
    this.modals.open(GoalComponent, {
      closeDisabled: true,
      data: {
        goalTemplate: 'test',
      },
      width: '512px',
    }).subscribe(() => {});
  }

  public confirmDeleteGoal() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
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

  public addCTTask() {
    this.modals.open(AddCTTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public editCTTask() {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public confirmDeleteCTTask() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
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
     'closeDisabled': true,
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
     'closeDisabled': true,
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
     'closeDisabled': true,
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
      closeDisabled: true,
      width: '768px',
    }).subscribe(() => {});
  }

  public editVital() {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public confirmDeleteVital() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
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
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public editMedication() {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public confirmDeleteMedication() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
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
      closeDisabled: true,
      width: '768px',
    }).subscribe(() => {});
  }

  public editStream() {
    this.modals.open(CreateStreamComponent, {
      closeDisabled: true,
      width: '640px',
    }).subscribe(() => {});
  }

  public confirmDeleteStream() {
    this.modals.open(ConfirmModalComponent, {
     'closeDisabled': true,
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
