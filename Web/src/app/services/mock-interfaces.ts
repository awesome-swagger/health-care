import * as moment from 'moment';

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  preferred_name?: string;
  phone?: string;
  gender?: string;
  birthdate?: string;
  image_url?: string;
}

export interface Organization {
  id: number;
  name: string;
  addr_street?: string;
  addr_suite?: string;
  addr_city?: string;
  addr_state?: string;
  addr_zip?: string;
}

export interface Facility {
  id: number;
  name: string;
  organization: Organization;
  is_affiliate: boolean;
  parent_company?: string;
  addr_street?: string;
  addr_suite?: string;
  addr_city?: string;
  addr_state?: string;
  addr_zip?: string;
}

export interface ProviderTitle {
  id: number;
  name: string;
  abbreviation: string;
}

export interface ProviderRole {
  id: number;
  name: string;
}

export interface ProviderSpecialty {
  id: number;
  name: string;
  physician_specialty: boolean;
}

export interface EmployeeProfile {
  id: number;
  user: User;
  status: string;
  npi_code?: string;
  organizations: Organization[];
  organizations_managed: Organization[];
  facilities: Facility[];
  facilities_managed: Facility[];
  title?: ProviderTitle;
  role?: ProviderRole;
  specialty?: ProviderSpecialty;
}

export interface Diagnosis {
  id: number;
  name: string;
  dx_code: string;
}

export interface Medication {
  id: number;
  name: string;
  rx_code: string;
}

export interface Procedure {
  id: number;
  name: string;
  px_code: string;
}

export interface Symptom {
  id: number;
  name: string;
  worst_label: string;
  best_label: string;
}

export interface PatientProfile {
  id: number;
  user: User;
  facility: Facility;
  emr_code?: string;
  status: string;
  diagnosis: Diagnosis[];
}

export interface ProblemArea {
  id: number;
  created: Date;
  modified: Date;
  date_identified: Date;
  name: string;
  description: string;
  patient: PatientProfile;
  identified_by: EmployeeProfile;
}

export interface PatientDiagnosis {
  id: number;
  type: string;
  date_identified: Date;
  diagnosing_practitioner: string;
  facility: string;
  patient: PatientProfile;
  diagnosis: Diagnosis;
}

export interface PatientProcedure {
  id: number;
  date_of_procedure: Date;
  attending_practitioner: string;
  facility: string;
  patient: PatientProfile;
  procedure: Procedure;
}

export interface PatientMedication {
  id: number;
  dose_mg: number;
  date_prescribed: Date;
  duration_days: number;
  instructions: string;
  prescribing_practitioner: string;
  patient: PatientProfile;
  procedure: Medication;
}

export interface CarePlanTemplate {
  id: number;
  created: Date;
  modified: Date;
  name: string;
  type: string;
  duration_weeks: number;
  is_active: boolean;
}

export interface CarePlan {
  id: number;
  created: Date;
  modified: Date;
  patient: PatientProfile;
  plan_template: CarePlanTemplate;
}

export interface PlanConsent {
  id: number;
  plan: CarePlan;
  created: Date;
  modified: Date;
  verbal_consent: boolean;
  discussed_co_pay: boolean;
  seen_within_year: boolean;
  will_use_mobile_app: boolean;
  will_interact_with_team: boolean;
  will_complete_tasks: boolean;
}

export interface CareTeamMember {
  id: number;
  employee_profile: EmployeeProfile;
  role: ProviderRole;
  plan: CarePlan;
}

export interface GoalTemplate {
  id: number;
  name: string;
  description: string;
  focus: string;
  start_on_day: number;
  duration_weeks: number;
  plan_template: CarePlanTemplate;
}

export interface Goal {
  id: number;
  plan: CarePlan;
  goal_template: GoalTemplate;
  created: Date;
  modified: Date;
}

export interface GoalProgress {
  id: number;
  goal: Goal;
  rating: number;
  created: Date;
  modified: Date;
}

export interface GoalComment {
  id: number;
  goal: Goal;
  user: User;
  content: string;
  created: Date;
  modified: Date;
}

export interface InfoMessageQueue {
  id: number;
  created: Date;
  modified: Date;
  name: string;
  type: string;
  plan_template: CarePlanTemplate;
}

export interface InfoMessage {
  id: number;
  text: string;
  queue: InfoMessageQueue;
}

export interface PatientTaskTemplate {
  id: number;
  start_on_day: number;
  frequency: string;
  repeat_amount: number;
  appear_time: string;
  due_time: string;
  name: string;
  plan_template: CarePlanTemplate;
}

export interface PatientTask {
  id: number;
  plan: CarePlan;
  patient_task_template: PatientTaskTemplate;
  appear_datetime: Date;
  due_datetime: Date;
  status: string;
  is_complete: boolean;
  state: string;
}

export interface TeamTaskTemplate {
  id: number;
  start_on_day: number;
  frequency: string;
  repeat_amount: number;
  appear_time: string;
  due_time: string;
  name: string;
  is_manager_task: boolean;
  category: string;
  plan_template: CarePlanTemplate;
  role?: ProviderRole;
}

export interface TeamTask {
  id: number;
  plan: CarePlan;
  team_task_template: TeamTaskTemplate;
  appear_datetime: Date;
  due_datetime: Date;
  status: string;
  is_complete: boolean;
  state: string;
}

export interface MedicationTaskTemplate {
  id: number;
  start_on_day: number;
  frequency: string;
  repeat_amount: number;
  appear_time: string;
  due_time: string;
  plan: CarePlan;
  patient_medication: PatientMedication;
}

export interface MedicationTask {
  id: number;
  plan: CarePlan;
  medication_task_template: MedicationTaskTemplate;
  appear_datetime: Date;
  due_datetime: Date;
  status: string;
  is_complete: boolean;
  state: string;
}

export interface SymptomTaskTemplate {
  id: number;
  start_on_day: number;
  frequency: string;
  repeat_amount: number;
  appear_time: string;
  due_time: string;
  plan_template: CarePlanTemplate;
}

export interface SymptomTask {
  id: number;
  plan: CarePlan;
  symptom_task_template: SymptomTaskTemplate;
  appear_datetime: Date;
  due_datetime: Date;
  comments: string;
  is_complete: boolean;
  state: string;
}

export interface SymptomRating {
  symptom_task: SymptomTask;
  symptom: Symptom;
  rating: number;
}

export interface AssessmentTaskTemplate {
  id: number;
  start_on_day: number;
  frequency: string;
  repeat_amount: number;
  appear_time: string;
  due_time: string;
  name: string;
  plan_template: CarePlanTemplate;
  tracks_outcome: boolean;
  tracks_satisfaction: boolean;
}

export interface AssessmentQuestion {
  id: number;
  prompt: string;
  worst_label: string;
  best_label: string;
  assessment_task_template: AssessmentTaskTemplate;
}

export interface AssessmentTask {
  id: number;
  plan: CarePlan;
  assessment_task_template: AssessmentTaskTemplate;
  appear_datetime: Date;
  due_datetime: Date;
  comments: string;
  is_complete: boolean;
  state: string;
}

export interface AssessmentResponse {
  id: number;
  assessment_task: AssessmentTask;
  assessment_question: AssessmentQuestion;
  rating: number;
}

export interface VitalTaskTemplate {
  id: number;
  start_on_day: number;
  frequency: string;
  repeat_amount: number;
  appear_time: string;
  due_time: string;
  name: string;
  plan_template: CarePlanTemplate;
}

export interface VitalTask {
  id: number;
  plan: CarePlan;
  vital_task_template: VitalTaskTemplate;
  appear_datetime: Date;
  due_datetime: Date;
  comments: string;
  is_complete: boolean;
}

export interface VitalQuestion {
  id: number;
  vital_task_template: VitalTaskTemplate;
  prompt: string;
  answer_type: string;
}

export interface VitalResponse {
  id: number;
  vital_task: VitalTask;
  question: VitalQuestion;
  answer_boolean?: boolean;
  answer_time?: string;
  answer_float?: number;
  answer_integer?: number;
  answer_scale?: number;
  answer_string?: string;
}
