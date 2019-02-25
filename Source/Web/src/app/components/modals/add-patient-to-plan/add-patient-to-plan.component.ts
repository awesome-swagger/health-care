import { Component, OnInit } from '@angular/core';
import { StoreService } from '../../../services/store.service';
import { ModalService } from '../../../modules/modals';
import { Subscription } from 'rxjs/Subscription';
import {
  filter as _filter,
  get as _get
} from 'lodash';

@Component({
  selector: 'app-add-patient-to-plan',
  templateUrl: './add-patient-to-plan.component.html',
  styleUrls: ['./add-patient-to-plan.component.scss'],
})
export class AddPatientToPlanComponent implements OnInit {

  public data = null;
  public action = 'add';
  public patientKnown = false;
  public patientInSystem = false;
  public createDiagnosis = false;
  public planKnown = false;
  public patients = [];
  public selectedPatient = null;
  public payerReimburses = false;
  public enrollPatientChecked = false;
  public newDiagnosis = '';
  public newDiagnosisIsChronic = false;
  public serviceAreas = [];
  public selectedServiceArea = null;
  public carePlans = [];
  public selectedPlan = null;
  public planTypes = ['BHI', 'CCM', 'CCCM', 'CoCM', 'RPM', 'TCM'];
  public selectedPlanType = 'BHI';
  public diagnoses = [
    {
      name: 'Diabetes',
      original: false,
      chronic: true,
    }
  ];
  public editDiagnosisIndex = -1;
  public firstName = '';
  public lastName = '';
  public phoneNumber = '';
  public facilities = [];
  public selectedFacility = null;
  public employees = [];
  public billingSearchString = '';
  public CMSearchString = '';
  public selectedBilling = null;
  public selectedCM = null;
  public careManagerRole = null;
  public billingPractitionerRole = null;

  public dropAPPM2Open;

  constructor(
    private store: StoreService,
    private modals: ModalService
  ) { }

  public ngOnInit() {
    console.log(this.data);
    this.data = this.data || {};
    if (this.data && Object.keys(this.data).length > 0) {
      this.action = this.data.action;
      this.patientKnown = this.data.patientKnown;
      this.patientInSystem = this.data.patientInSystem;
      this.planKnown = this.data.planKnown;

      if (!this.data.facility) {
        this.store.Facility.readListPaged().subscribe(res => {
          this.facilities = res;
        })
      } else {
        this.selectedFacility = this.data.facility;
      }

      if (this.patientKnown) {
        this.selectedPatient = this.data.patient;
      }
    }
    this.getPatients().then((patients: any) => {
      this.patients = patients;
    });
    this.getCarePlanTemplates().then((plans: any) => {
      this.carePlans = plans;
      this.getServiceAreas().then((serviceAreas: any) => {
        this.serviceAreas = serviceAreas;
        if (this.planKnown) {
          this.selectedPlan = this.carePlans.find((obj) => obj.id === this.data.planTemplate.id);
          this.selectedServiceArea = this.serviceAreas.find((obj) => obj.id === this.data.planTemplate.service_area.id);
        }
      });
    });

    this.store.ProviderRole.readListPaged().subscribe(res => {
      res.forEach(role => {
        if (role.name === 'Care Manager' || role.name === 'Care Team Manager') {
          this.careManagerRole = role;
        }
        if (role.name === 'Billing Practitioner') {
          this.billingPractitionerRole = role;
        }
      })
    })

    this.store.EmployeeProfile.readListPaged().subscribe(res => {
      this.employees = res;
    })
  }

  public getPatients() {
    return new Promise((resolve, reject) => {
        let patientsSub = this.store.PatientProfile.readListPaged().subscribe(
          (patients) => {
            resolve(patients);
          },
          (err) => {
            reject(err);
          },
          () => {
            patientsSub.unsubscribe();
          }
        )
    });
  }

  public getServiceAreas() {
    return new Promise((resolve, reject) => {
        let serviceAreasSub = this.store.ServiceArea.readListPaged().subscribe(
          (serviceAreas) => {
            resolve(serviceAreas);
          },
          (err) => {
            reject(err);
          },
          () => {
            serviceAreasSub.unsubscribe();
          }
        )
    });
  }

  public getCarePlanTemplates() {
    return new Promise((resolve, reject) => {
        let carePlanSub = this.store.CarePlanTemplate.readListPaged().subscribe(
          (plans) => {
            resolve(plans);
          },
          (err) => {
            reject(err);
          },
          () => {
            carePlanSub.unsubscribe();
          }
        )
    });
  }

  public carePlansFiltered() {
    if (!this.selectedServiceArea) {
      return [];
    }
    return this.carePlans.filter((obj) => obj.service_area.id === this.selectedServiceArea.id);
  }

  public selectedPatientName() {
    if (!this.selectedPatient) {
      return '';
    }
    return `${this.selectedPatient.user.first_name} ${this.selectedPatient.user.last_name}`;
  }

  public addDiagnosis() {
    this.createDiagnosis = !this.createDiagnosis
    this.diagnoses.push({
      name: this.newDiagnosis,
      original: false,
      chronic: this.newDiagnosisIsChronic,
    });
  }

  public editDiagnosis(index) {
    this.editDiagnosisIndex = index;
  }

  public clickClose() {
    this.modals.close(null);
  }

  public get saveDisabled() {
    if (this.enrollPatientChecked && !this.payerReimburses) {
      return !this.selectedPlan || !this.selectedPatient || !this.selectedCM;
    } else if (this.enrollPatientChecked && this.payerReimburses) {
      return !this.selectedPlan || !this.selectedPatient || !this.selectedCM || !this.selectedBilling;
    } else if (!this.enrollPatientChecked) {
      return !this.firstName || !this.lastName;
    }
  }

  public handleSubmit() {
    if (!this.enrollPatientChecked) {
      let potentialPatientSub = this.store.PotentialPatient.create({
        first_name: this.firstName,
        last_name: this.lastName,
        care_plan: this.selectedPlan.name,
        phone: this.phoneNumber,
        facility: [
          this.selectedFacility.id,
			  ],
      }).subscribe(
        (data) => {
          this.modals.close(data);
        },
        (err) => {

        },
        () => {
          potentialPatientSub.unsubscribe();
        }
      )
    }

    if (this.enrollPatientChecked) {
      this.store.CarePlan.create({
        patient: this.selectedPatient.id,
        plan_template: this.selectedPlan.id,
      }).subscribe(carePlan => {
        this.store.CareTeamMember.create({
          employee_profile: this.selectedCM.id,
          role: this.careManagerRole.id,
          plan: carePlan.id,
          is_manager: true,
        }).subscribe(res => {
          carePlan.careTeam = [res];
          if (this.payerReimburses && this.billingPractitionerRole && this.selectedBilling) {
            this.store.CareTeamMember.create({
              employee_profile: this.selectedBilling.id,
              role: this.billingPractitionerRole.id,
              plan: carePlan.id,
              is_manager: false,
            }).subscribe(res => {
              carePlan.careTeam.push(res);
              this.modals.close(carePlan);
            })
          } else {
            this.modals.close(carePlan);
          }
        })
      })
    }
  }

  get searchBillingEmployees() {
    if (this.billingSearchString.length >= 3) {
      return _filter(this.employees, employee => {
        const name = `${_get(employee, 'user.first_name')} ${_get(employee, 'user.last_name')}`;
        return name.indexOf(this.billingSearchString) > -1;
      })
    }
    return [];
  }

  get searchCMEmployees() {
    if (this.CMSearchString.length >= 3) {
      return _filter(this.employees, employee => {
        const name = `${_get(employee, 'user.first_name')} ${_get(employee, 'user.last_name')}`;
        return name.indexOf(this.CMSearchString) > -1;
      })
    }
    return [];
  }

  public setBillingPractitioner(employee) {
    this.selectedBilling = employee;
    this.billingSearchString = `${employee.user.first_name} ${employee.user.last_name}`;
  }

  public setCareManager(employee) {
    this.selectedCM = employee;
    this.CMSearchString = `${employee.user.first_name} ${employee.user.last_name}`;
  }
}
