import { Injectable } from '@angular/core';
import * as faker from 'faker';
import * as moment from 'moment';
import { groupBy as _groupBy } from 'lodash';

import {
  User,
  Organization,
  Facility,
  ProviderTitle,
  ProviderRole,
  ProviderSpecialty,
  EmployeeProfile,
  Diagnosis,
  Medication,
  Procedure,
  Symptom,
  PatientProfile,
  ProblemArea,
  PatientDiagnosis,
  PatientProcedure,
  PatientMedication,
  CarePlanTemplate,
  CarePlan,
  PlanConsent,
  CareTeamMember,
  GoalTemplate,
  Goal,
  GoalProgress,
  GoalComment,
  InfoMessageQueue,
  InfoMessage,
  PatientTaskTemplate,
  PatientTask,
  TeamTaskTemplate,
  TeamTask,
  MedicationTaskTemplate,
  MedicationTask,
  SymptomTaskTemplate,
  SymptomTask,
  SymptomRating,
  AssessmentTaskTemplate,
  AssessmentQuestion,
  AssessmentTask,
  AssessmentResponse,
  VitalTaskTemplate,
  VitalTask,
  VitalQuestion,
  VitalResponse,
} from './mock-interfaces';

import { MockStore } from './mock-store';

@Injectable()
export class MockService {

  public Users = new MockStore<User>();
  public Organizations = new MockStore<Organization>();
  public Facilities = new MockStore<Facility>();
  public ProviderTitles = new MockStore<ProviderTitle>();
  public ProviderRoles = new MockStore<ProviderRole>();
  public ProviderSpecialties = new MockStore<ProviderSpecialty>();
  public EmployeeProfiles = new MockStore<EmployeeProfile>();
  public Diagnosis = new MockStore<Diagnosis>();
  public Medications = new MockStore<Medication>();
  public Procedures = new MockStore<Procedure>();
  public Symptoms = new MockStore<Symptom>();
  public PatientProfiles = new MockStore<PatientProfile>();
  public ProblemAreas = new MockStore<ProblemArea>();
  public PatientDiagnosis = new MockStore<PatientDiagnosis>();
  public PatientProcedures = new MockStore<PatientProcedure>();
  public PatientMedications = new MockStore<PatientMedication>();
  public CarePlanTemplates = new MockStore<CarePlanTemplate>();
  public CarePlans = new MockStore<CarePlan>();
  public PlanConsents = new MockStore<PlanConsent>();
  public CareTeamMembers = new MockStore<CareTeamMember>();
  public GoalTemplates = new MockStore<GoalTemplate>();
  public Goals = new MockStore<Goal>();
  public GoalProgressUpdates = new MockStore<GoalProgress>();
  public GoalComments = new MockStore<GoalComment>();
  public InfoMessageQueues = new MockStore<InfoMessageQueue>();
  public InfoMessages = new MockStore<InfoMessage>();
  public PatientTaskTemplates = new MockStore<PatientTaskTemplate>();
  public PatientTasks = new MockStore<PatientTask>();
  public TeamTaskTemplates = new MockStore<TeamTaskTemplate>();
  public TeamTasks = new MockStore<TeamTask>();
  public MedicationTaskTemplates = new MockStore<MedicationTaskTemplate>();
  public MedicationTask = new MockStore<MedicationTask>();
  public SymptomTaskTemplates = new MockStore<SymptomTaskTemplate>();
  public SymptomTasks = new MockStore<SymptomTask>();
  public SymptomRatings = new MockStore<SymptomRating>();
  public AssessmentTaskTemplates = new MockStore<AssessmentTaskTemplate>();
  public AssessmentQuestions = new MockStore<AssessmentQuestion>();
  public AssessmentTasks = new MockStore<AssessmentTask>();
  public AssessmentResponses = new MockStore<AssessmentResponse>();
  public VitalTaskTemplates = new MockStore<VitalTaskTemplate>();
  public VitalTasks = new MockStore<VitalTask>();
  public VitalQuestions = new MockStore<VitalQuestion>();
  public VitalResponses = new MockStore<VitalResponse>();

  constructor() {
    let ogdenClinic = this.Organizations.create({
      name: 'Ogden Clinic',
      addr_street: '1491 East Ridgeline Dr',
      addr_city: 'Ogden',
      addr_state: 'UT',
      addr_zip: '84404',
    });
    this.Facilities.create({
      name: 'Canyon View',
      organization: ogdenClinic,
      is_affiliate: false,
      addr_street: '1159 East 12th Street',
      addr_city: 'Ogden',
      addr_state: 'UT',
      addr_zip: '84404',
    });
    this.Facilities.create({
      name: 'Davis Family Physicians',
      organization: ogdenClinic,
      is_affiliate: true,
      addr_street: '3225W Gordon Ave',
      addr_suite: 'Suite1',
      addr_city: 'Layton',
      addr_state: 'UT',
      addr_zip: '84041',
    });
    this.ProviderTitles.create({
      name: 'Care Coordinator',
      abbreviation: 'CC',
    });
    this.ProviderTitles.create({
      name: 'Medical Doctor',
      abbreviation: 'MD',
    });
    this.ProviderTitles.create({
      name: 'Care Manager',
      abbreviation: 'CM',
    });
    this.ProviderTitles.create({
      name: 'Dietician',
      abbreviation: 'DT',
    });
    let depressionPlan = this.CarePlanTemplates.create({
      created: faker.date.past(),
      modified: faker.date.past(),
      name: 'Depression',
      type: 'ccm',
      duration_weeks: 12,
      is_active: true,
    });
    this.GoalTemplates.create({
      name: 'Manage Depression Symptoms',
      description: 'Keep depression from controlling attitudes and behavior.',
      focus: 'Manage negative thoughts',
      start_on_day: 0,
      duration_weeks: -1,
      plan_template: depressionPlan,
    });
    this.PatientTaskTemplates.create({
      start_on_day: this.randomNumber(0, 7),
      frequency: 'every_other_day',
      repeat_amount: -1,
      appear_time: '09:00:00',
      due_time: '17:00:00',
      name: 'Call Doctor',
      plan_template: depressionPlan,
    });
    this.TeamTaskTemplates.create({
      start_on_day: this.randomNumber(0, 7),
      frequency: 'every_other_day',
      repeat_amount: -1,
      appear_time: '09:00:00',
      due_time: '17:00:00',
      name: 'Check Vital Reports',
      category: 'interaction',
      is_manager_task: true,
      plan_template: depressionPlan,
    });
    this.SymptomTaskTemplates.create({
      start_on_day: this.randomNumber(0, 7),
      frequency: 'every_other_day',
      repeat_amount: -1,
      appear_time: '09:00:00',
      due_time: '17:00:00',
      plan_template: depressionPlan,
    });
    this.SymptomTaskTemplates.create({
      start_on_day: this.randomNumber(0, 7),
      frequency: 'every_other_day',
      repeat_amount: -1,
      appear_time: '09:00:00',
      due_time: '17:00:00',
      plan_template: depressionPlan,
    });
    this.AssessmentTaskTemplates.create({
      start_on_day: this.randomNumber(0, 7),
      frequency: 'every_other_day',
      repeat_amount: -1,
      appear_time: '09:00:00',
      due_time: '17:00:00',
      plan_template: depressionPlan,
      name: 'Depression Assessment',
      tracks_outcome: false,
      tracks_satisfaction: false,
    });
    let sleepVitalTaskTemplate = this.VitalTaskTemplates.create({
      start_on_day: this.randomNumber(0, 7),
      frequency: 'every_other_day',
      repeat_amount: -1,
      appear_time: '09:00:00',
      due_time: '17:00:00',
      plan_template: depressionPlan,
      name: 'Sleep',
    });
    this.VitalQuestions.create({
      vital_task_template: sleepVitalTaskTemplate,
      prompt: 'Time you went to bed',
      answer_type: 'time',
    });
    this.VitalQuestions.create({
      vital_task_template: sleepVitalTaskTemplate,
      prompt: 'Time you got up',
      answer_type: 'time',
    });
    this.VitalQuestions.create({
      vital_task_template: sleepVitalTaskTemplate,
      prompt: 'How many times did you wake up during the night?',
      answer_type: 'integer',
    });
    this.VitalQuestions.create({
      vital_task_template: sleepVitalTaskTemplate,
      prompt: 'Rate your quality of sleep',
      answer_type: 'scale',
    });
    this.VitalQuestions.create({
      vital_task_template: sleepVitalTaskTemplate,
      prompt: 'How did you feel when you got up?',
      answer_type: 'scale',
    });
    // Create Random Employees
    for (let i = 0; i < 45; i++) {
      this.createRandomEmployee();
    }
    // Create Random Patients
    for (let i = 0; i < 100; i++) {
      this.createRandomPatient();
    }
    // For all active patients create a random number (between 1 and 3) of care plans.
    this.getPatientsGroupedByStatus()['active'].forEach((patient) => {
      for (let i = 0; i <= this.randomNumber(1, 3); i++) {
        this.createCarePlanForPatient(patient, depressionPlan);
      }
    });
  }

  public randomNumber(min, max) {
    return Math.floor(Math.random() * max) + min;
  }

  public createRandomUser() {
    let firstName = faker.name.firstName();
    let lastName = faker.name.lastName();
    return this.Users.create({
      email: `${firstName.toLowerCase()}@${lastName.toLowerCase()}.com`,
      first_name: firstName,
      last_name: lastName,
      phone: faker.phone.phoneNumber(),
      image_url: faker.image.avatar(),
    });
  }

  public createRandomEmployee() {
    let statusChoices = ['invited', 'inactive', 'active'];
    let organizations = this.Organizations.readList();
    let facilities = this.Facilities.readList();
    let titles = this.ProviderTitles.readList();
    let randomOrganization = organizations[this.randomNumber(0, organizations.length)];
    let randomFacility = facilities[this.randomNumber(0, facilities.length)];
    return this.EmployeeProfiles.create({
      user: this.createRandomUser(),
      status: statusChoices[this.randomNumber(0, statusChoices.length)],
      organizations: [randomOrganization],
      organizations_managed: [],
      facilities: [randomFacility],
      facilities_managed: [],
      title: titles[this.randomNumber(0, titles.length)],
    });
  }

  public createRandomPatient() {
    let statusChoices = ['pre-potential', 'potential', 'invited', 'delinquent', 'inactive', 'active'];
    let facilities = this.Facilities.readList();
    return this.PatientProfiles.create({
      user: this.createRandomUser(),
      status: statusChoices[this.randomNumber(0, statusChoices.length)],
      facility: facilities[this.randomNumber(0, facilities.length)],
      diagnosis: [],
    });
  }

  public createCarePlanForPatient(patient, template) {
    this.CarePlans.create({
      created: faker.date.past(),
      modified: faker.date.past(),
      patient: patient,
      plan_template: template,
    });
  }

  public getPatientsGroupedByStatus() {
    let patients = this.PatientProfiles.readList();
    let patientGroupDefaults = {
      'pre-potential': null,
      'potential': null,
      'invited': null,
      'delinquent': null,
      'inactive': null,
      'active': null,
    };
    let groupedByStatus = _groupBy(patients, (obj) => {
      return obj.status;
    });
    return Object.assign({}, patientGroupDefaults, groupedByStatus);
  }

  public groupPatientsByFacility(patients) {
    let groupedByFacility = _groupBy(patients, (obj) => {
      return obj.facility.id;
    });
    return groupedByFacility;
  }
}
