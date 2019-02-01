import { Component, OnInit, OnDestroy, ViewEncapsulation } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { ToastService } from '../../modules/toast';
import { AuthService, HttpService, StoreService } from '../../services';
import { EditTaskComponent } from '../../components/modals/edit-task/edit-task.component';
import { PreviewVitalComponent } from '../../components/modals/preview-vital/preview-vital.component';
import { CreateVitalComponent } from '../../components/modals/create-vital/create-vital.component';
import { CreateAssessmentComponent } from '../../components/modals/create-assessment/create-assessment.component';
import { CreateStreamComponent } from '../../components/modals/create-stream/create-stream.component';
import { EnrollmentRequiredComponent } from '../../components/modals/enrollment-required/enrollment-required.component';
import { PatientEnrolledComponent } from '../../components/modals/patient-enrolled/patient-enrolled.component';
import { PlanExpiredComponent } from '../../components/modals/plan-expired/plan-expired.component';
import { PlanLimitReachedComponent } from '../../components/modals/plan-limit-reached/plan-limit-reached.component';
import { PercentageGaugeComponent } from '../../components/graphs/percentage-gauge/percentage-gauge.component';
import { ResultsGraphComponent } from '../../components/graphs/results-graph/results-graph.component';
import { ActivePatientsGraphComponent } from '../../components/graphs/active-patients-graph/active-patients-graph.component';
import { PatientsEnrolledGraphComponent } from '../../components/graphs/patients-enrolled-graph/patients-enrolled-graph.component';

@Component({
  selector: 'app-styleguide',
  templateUrl: './styleguide.component.html',
  styleUrls: ['./styleguide.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class StyleguideComponent implements OnInit {

  public user: Observable<any> = this.auth.user$;

  public showDate;
  public multiOpen;
  public dropOpen;
  public tooltip1Open;
  public tooltip2Open;
  public accord1Open;
  public tooltip3Open;
  public tooltip4Open;
  public tooltip5Open;
  public accord2Open;

  public datepickerOptions = {
    //relativeLeft: '-310px',
  };

  public constructor(
    private modals: ModalService,
    private toast: ToastService,
    private auth: AuthService,
    private http: HttpService,
    private store: StoreService,
  ) { }

  public ngOnInit() { }

  public openConfirm() {
    this.modals.open(ConfirmModalComponent, {
      'backdrop': true,
      'closeDisabled': false,
      'width': '384px',
      'height': 'auto',
      'data': {
        'title': 'Are You Sure?',
        'body': 'This is an example of a confirm modal. Do you agree?',
        'okText': 'Yes',
        'cancelText': 'No',
      }
    }).subscribe((r) => {
      this.toast.success(`Clicked ${r}`);
    });
  }

  public editTask() {
    this.modals.open(EditTaskComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public previewVital() {
    this.modals.open(PreviewVitalComponent, {
      closeDisabled: true,
      width: '432px',
    }).subscribe(() => {});
  }

  public createVital() {
    this.modals.open(CreateVitalComponent, {
      closeDisabled: true,
      width: '976px',
    }).subscribe(() => {});
  }

  public createAssessment() {
    this.modals.open(CreateAssessmentComponent, {
      closeDisabled: true,
      width: '960px',
    }).subscribe(() => {});
  }

  public createStream() {
    this.modals.open(CreateStreamComponent, {
      closeDisabled: true,
      width: '640px',
    }).subscribe(() => {});
  }

  public enrollmentRequired() {
    this.modals.open(EnrollmentRequiredComponent, {
      closeDisabled: true,
      width: '416px',
    }).subscribe(() => {});
  }

  public patientEnrolled() {
    this.modals.open(PatientEnrolledComponent, {
      closeDisabled: true,
      width: '384px',
    }).subscribe(() => {});
  }

  public planExpired() {
    this.modals.open(PlanExpiredComponent, {
      closeDisabled: false,
      width: '384px',
    }).subscribe(() => {});
  }

  public planLimitReached() {
    this.modals.open(PlanLimitReachedComponent, {
      closeDisabled: false,
      width: '384px',
    }).subscribe(() => {});
  }
}
