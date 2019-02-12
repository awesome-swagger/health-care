import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {
  BillingComponent,
  DashboardComponent,
  ErrorComponent,
  FacilityComponent,
  InviteComponent,
  CreateAccountComponent,
  LoginComponent,
  ResetPasswordComponent,
  VerifyEmailComponent,
  OrganizationComponent,
  PatientComponent,
  PatientDashboardComponent,
  PatientDetailsComponent,
  PatientHistoryComponent,
  PatientMessagingComponent,
  PatientOverviewComponent,
  PatientTeamComponent,
  ActivePatientsComponent,
  InvitedPatientsComponent,
  PotentialPatientsComponent,
  InactivePatientsComponent,
  PlansComponent,
  PlanInfoComponent,
  PlanScheduleComponent,
  StyleguideComponent,
  UserComponent,
  UsersComponent,
  AllModalsComponent,
} from './routes';
import { CanActivateViaAuthGuard } from './services';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full',
  },
  {
    path: 'modals',
    component: AllModalsComponent,
    data: { title: 'Modals' },
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
    data: { title: 'Dashboard' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'billing',
    component: BillingComponent,
    data: { title: 'Billing' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'facility',
    component: FacilityComponent,
    data: { title: 'Facility' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'invite',
    component: InviteComponent,
    data: { title: 'Invite Users' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'create-account',
    component: CreateAccountComponent,
    data: { title: 'Create Account' },
  },
  {
    path: 'login',
    component: LoginComponent,
    data: { title: 'Login' },
  },
  {
    path: 'reset-password',
    component: ResetPasswordComponent,
    data: { title: 'Reset Password' },
  },
  {
    path: 'verify-email',
    component: VerifyEmailComponent,
    data: { title: 'Verify Email' },
  },
  {
    path: 'organization',
    component: OrganizationComponent,
    data: { title: 'Organization' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patient/:patientId',
    component: PatientComponent,
    data: { title: 'Patient', },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patient/:patientId/dashboard/:planId',
    component: PatientDashboardComponent,
    data: { title: 'Patient Dashboard', },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patient/:patientId/details/:planId',
    component: PatientDetailsComponent,
    data: { title: 'Patient Details', },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patient/:patientId/messaging/:planId',
    component: PatientMessagingComponent,
    data: { title: 'Patient Messaging', },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patient/:patientId/overview/:planId',
    component: PatientOverviewComponent,
    data: { title: 'Patient Overview', },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patient/:patientId/team/:planId',
    component: PatientTeamComponent,
    data: { title: 'Patient Care Team', },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patient/:patientId/history/:planId',
    component: PatientHistoryComponent,
    data: { title: 'Patient History', },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patients/active',
    component: ActivePatientsComponent,
    data: { title: 'Active Patients' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patients/invited',
    component: InvitedPatientsComponent,
    data: { title: 'Invited Patients' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patients/potential',
    component: PotentialPatientsComponent,
    data: { title: 'Potential Patients' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'patients/inactive',
    component: InactivePatientsComponent,
    data: { title: 'Inactive Patients' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'plans',
    component: PlansComponent,
    data: { title: 'Plans' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'plan/:id/info',
    component: PlanInfoComponent,
    data: { title: 'Plans' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'plan/:id/info',
    component: PlanInfoComponent,
    data: { title: 'Plan Info' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'plan/:id/schedule',
    component: PlanScheduleComponent,
    data: { title: 'Plans Schedule' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'users',
    component: UsersComponent,
    data: { title: 'Users' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: 'user/:id',
    component: UserComponent,
    data: { title: 'User' },
    canActivate: [ CanActivateViaAuthGuard ],
  },
  {
    path: '**',
    component: ErrorComponent,
    data: { title: 'Page Not Found' },  // because title str should differ from path str
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
