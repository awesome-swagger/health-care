import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NavbarService, StoreService } from '../../services';
import { EditFacilityComponent } from '../organization/modals/edit-facility.component';
import { AddUserComponent } from '../users/invite/modals/add-user.component';
import { ChangeEmailComponent } from '../users/detail/modals/change-email/change-email.component';
import { ChangePasswordComponent } from '../users/detail/modals/change-password/change-password.component';
import { AddPlanComponent } from '../plans/modals/add-plan/add-plan.component';
import { PlanDurationComponent } from '../../components/modals/plan-duration/plan-duration.component';
import { GoalComponent } from '../../components/modals/goal/goal.component';
import { RecordResultsComponent } from '../../components/modals/record-results/record-results.component';
import { AddCTTaskComponent } from '../../components/modals/add-ct-task/add-ct-task.component';
import { EditTaskComponent } from '../../components/modals/edit-task/edit-task.component';
import { AddVitalComponent } from '../../components/modals/add-vital/add-vital.component';
import { CreateVitalComponent } from '../../components/modals/create-vital/create-vital.component';
import { PreviewVitalComponent } from '../../components/modals/preview-vital/preview-vital.component';
import { AddAssessmentComponent } from '../../components/modals/add-assessment/add-assessment.component';
import { CreateAssessmentComponent } from '../../components/modals/create-assessment/create-assessment.component';
import { AddStreamComponent } from '../../components/modals/add-stream/add-stream.component';
import { CreateStreamComponent } from '../../components/modals/create-stream/create-stream.component';
import { DeletePlanComponent } from '../plans/modals/delete-plan/delete-plan.component';
import { ReminderEmailComponent } from '../patients/invited/modals/reminder-email/reminder-email.component';
import { AddPatientToPlanComponent } from '../../components/modals/add-patient-to-plan/add-patient-to-plan.component';
import { ModalService, ConfirmModalComponent } from '../../modules/modals';
import { ReassignBillingPractitionerComponent } from '../users/modals/reassign-billing-practitioner/reassign-billing-practitioner.component';
import { EnrollPatientComponent } from '../patient/modals/enroll-patient/enroll-patient.component';
import { CarePlanConsentComponent } from '../patient/modals/care-plan-consent/care-plan-consent.component';
import { FinancialDetailsComponent } from '../patient/modals/financial-details/financial-details.component';
import { ProblemAreasComponent } from '../patient/modals/problem-areas/problem-areas.component';
import { AddDiagnosisComponent } from '../patient/modals/add-diagnosis/add-diagnosis.component';
import { EditDiagnosisComponent } from '../patient/modals/edit-diagnosis/edit-diagnosis.component';
import { AddProcedureComponent } from '../patient/modals/add-procedure/add-procedure.component';
import { EditProcedureComponent } from '../patient/modals/edit-procedure/edit-procedure.component';
import { MedicationComponent } from '../patient/modals/medication/medication.component';
import { AddCtComponent } from '../patient/modals/add-ct/add-ct.component';
import { EditBillingPractitionerComponent } from '../patient/modals/edit-billing-practitioner/edit-billing-practitioner.component';
import { EditCcmComponent } from '../patient/modals/edit-ccm/edit-ccm.component';

@Component({
  selector: 'app-all-modals',
  templateUrl: './all-modals.component.html',
  styleUrls: ['./all-modals.component.scss']
})
export class AllModalsComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
    private nav: NavbarService,
  ) { }

  ngOnInit() {
  }

  public openAddFacility() {
    this.modals.open(EditFacilityComponent, {
      closeDisabled: true,
      data: {
        type: 'add',
        isAffiliate: false,
        facility: {},
        isOrganization: false,
      },
      width: '512px',
    })
  }

  public openEditFacility() {
    this.modals.open(EditFacilityComponent, {
      closeDisabled: true,
      data: {
        type: 'edit',
        isAffiliate: false,
        facility: {},
        isOrganization: false,
      },
      width: '512px',
    }).subscribe(() => {});
  }

  public openDeleteFacility() {
    this.modals.open(ConfirmModalComponent, {
      data: {
        title: 'Are You Sure?',
        body: 'Are you sure you want to delete this facility? This would remove 28 user accounts and 468 active patients.',
        okText: 'Continue',
        cancelText: 'Cancel',
      },
      width: '440px',
    }).subscribe(() => {});
  }

  public openAddUser() {
    this.modals.open(AddUserComponent, {
      width: '512px',
    })
  }

  public openReassignBillingPractitioner() {
    this.modals.open(ReassignBillingPractitionerComponent, {
      width: '741px',
    })
  }

  public openChangeEmail() {
    this.modals.open(ChangeEmailComponent, {
      width: '440px',
    })
  }

  public openChangePassword() {
    this.modals.open(ChangePasswordComponent, {
      width: '440px',
    })
  }

  public openAddPlan() {
    this.modals.open(AddPlanComponent, {
      width: '440px',
      overflow: 'visible',
    })
  }

  public openPlanDuration() {
    this.modals.open(PlanDurationComponent, {
      width: '440px',
    })
  }

  public openGoal() {
    this.modals.open(GoalComponent, {
      width: '440px',
    })
  }

  public openAddCTTask() {
    this.modals.open(AddCTTaskComponent, {
      width: '440px',
    })
  }

  public openEditTask() {
    this.modals.open(EditTaskComponent, {
      width: '440px',
    })
  }

  public openAddVital() {
    this.modals.open(AddVitalComponent, {
      width: '741px',
    })
  }

  public openCreateVital() {
    this.modals.open(CreateVitalComponent, {
      width: '784px',
    })
  }

  public openPreviewVital() {
    this.modals.open(PreviewVitalComponent, {
      width: '440px',
    })
  }

  public openAddAssessment() {
    this.modals.open(AddAssessmentComponent, {
      width: '741px',
    })
  }

  public openCreateAssessment() {
    this.modals.open(CreateAssessmentComponent, {
      width: '741px',
    })
  }

  public openAddStream() {
    this.modals.open(AddStreamComponent, {
      width: '741px',
    })
  }

  public openCreateStream() {
    this.modals.open(CreateStreamComponent, {
      width: '741px',
    })
  }

  public openDeletePlan() {
    this.modals.open(DeletePlanComponent, {
      width: '1000px',
    })
  }

  public openReminderEmail() {
    this.modals.open(ReminderEmailComponent, {
      width: '440px',
    })
  }

  public openAddPatientToPlan() {
    this.modals.open(AddPatientToPlanComponent, {
      width: '741px',
    })
  }

  public openEnrollPatient() {
    this.modals.open(EnrollPatientComponent, {
      width: '512px',
      overflowX: 'visible',
      data: {
        patientName: 'Alexander Montgomery',
        patientPhone: '(555)555-5555',
        carePlan: 'Heart Disease',
        carePlanType: 'RPM',
      }
    })
  }

  public openCarePlanConsent() {
    this.modals.open(CarePlanConsentComponent, {
      width: '512px',
      data: {
        patientName: 'Alexander Montgomery',
      },
    })
  }

  public openFinancialDetails() {
    this.modals.open(FinancialDetailsComponent, {
      width: '440px',
      data: {
        carePlan: 'CoCM',
      },
    })
  }

  public openProblemAreas() {
    this.modals.open(ProblemAreasComponent, {
      width: '741px',
      data: {
        currentUser: 'Lori Ramirez, RN',
      }
    })
  }

  public openAddDiagnosis() {
    this.modals.open(AddDiagnosisComponent, {
      width: '440px',
    })
  }

  public openEditDiagnosis() {
    this.modals.open(EditDiagnosisComponent, {
      width: '512px',
    })
  }

  public openAddProcedure() {
    this.modals.open(AddProcedureComponent, {
      width: '440px',
    })
  }

  public openEditProcedure() {
    this.modals.open(EditProcedureComponent, {
      width: '512px',
    })
  }

  public openGoalUpdate() {
    this.modals.open(GoalComponent, {
      width: '512px',
      data: {
        update: true,
        patientName: 'Theresa Beckstrom',
      },
    })
  }

  public openRecordResults() {
    this.modals.open(RecordResultsComponent, {
      width: '512px',
    })
  }

  public openEditMedication() {
    this.modals.open(MedicationComponent, {
      width: '512px',
    })
  }

  public openAddCt() {
    this.modals.open(AddCtComponent, {
      width: '440px',
    })
  }

  public openEditBillingPractitioner() {
    this.modals.open(EditBillingPractitionerComponent, {
      width: '440px',
    })
  }

  public openEditCmm() {
    this.modals.open(EditCcmComponent, {
      width: '440px',
    })
  }

}
