import { Component, OnInit } from '@angular/core';
import { StoreService } from '../../../services/store.service';
import { ModalService } from '../../../modules/modals';
import { Subscription } from 'rxjs/Subscription';
import {
  filter as _filter,
  get as _get,
  uniqWith as _uniqWith,
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
  public potentialPatients = [];
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
  public email = '';
  public facilities = [];
  public selectedFacility = null;
  public employees = [];
  public billingSearchString = '';
  public CMSearchString = '';
  public selectedBilling = null;
  public selectedCM = null;
  public careManagerRole = null;
  public billingPractitionerRole = null;
  public source = '';

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
      this.enrollPatientChecked = this.data.enrollPatientChecked;
      this.store.Facility.readListPaged().subscribe(res => {
        this.facilities = res;
        if (this.data.potentialPatient) {
          this.selectedFacility = this.facilities.find(f => f.id === this.data.potentialPatient.facility[0]);
        }
      })

      if (this.data.facility) {
        this.selectedFacility = this.data.facility;
      }

      if (this.data.patient) {
        this.selectedPatient = this.data.patient;
        this.firstName = this.data.patient.user.first_name;
        this.lastName = this.data.patient.user.last_name;
        this.phoneNumber = this.data.patient.user.phone;
        this.email = this.data.patient.user.email;
        this.selectedFacility = this.data.patient.facility;
      }

      if (this.data.potentialPatient) {
        this.firstName = this.data.potentialPatient.first_name;
        this.lastName = this.data.potentialPatient.last_name;
        this.phoneNumber = this.data.potentialPatient.phone;
        this.source = this.data.potentialPatient.source;
      }
    }
    this.getPatients().then((patients: any) => {
      if (this.selectedFacility) {
        this.patients = patients.filter(p => p.facility.id === this.selectedFacility.id);
      } else {
        this.patients = patients;
      }
    });
    this.store.PotentialPatient.readListPaged().subscribe(res => {
      if (this.selectedFacility) {
        this.potentialPatients = _uniqWith(res, (a, b) => a.first_name === b.first_name && a.last_name === b.last_name)
          .filter(p => p.facility[0] === this.selectedFacility.id);
      }
      this.potentialPatients = _uniqWith(res, (a, b) => a.first_name === b.first_name && a.last_name === b.last_name);
    })

    this.getCarePlanTemplates().then((plans: any) => {
      this.carePlans = plans;
      this.getServiceAreas().then((serviceAreas: any) => {
        this.serviceAreas = serviceAreas;
        if (this.planKnown && this.data.planTemplate) {
          this.selectedPlan = this.carePlans.find((obj) => obj.id === this.data.planTemplate.id);
          this.selectedServiceArea = this.serviceAreas.find((obj) => obj.id === this.data.planTemplate.service_area.id);
        }
        if (this.planKnown && this.data.potentialPatient) {
          this.selectedPlan = this.data.potentialPatient.care_plan;
          this.selectedServiceArea = this.data.potentialPatient.care_plan.service_area;
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

  public selectPatient(patient) {
    this.selectedPatient = patient;
    this.firstName = patient.user.first_name;
    this.lastName = patient.user.last_name;
    this.phoneNumber = patient.user.phone;
    this.email = patient.user.email;

    if (patient.facility[0] && typeof patient.facility[0] === 'string') {
      this.selectedFacility = this.facilities.find(f => f.id === patient.facility[0])
    } else {
      this.selectedFacility = patient.facility;
    }
  }

  public unselectPatient() {
    this.selectedPatient = null;
    this.firstName = '';
    this.lastName = '';
    this.phoneNumber = '';
    this.email = '';
    this.selectedFacility = null;
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

    if (this.firstName && this.lastName && this.email && this.selectedPlan && this.selectedCM && this.selectedFacility) {
      return false;
    }

    if (this.enrollPatientChecked && !this.payerReimburses) {
      return !this.selectedPlan || !this.selectedPatient || !this.selectedCM;
    } else if (this.enrollPatientChecked && this.payerReimburses) {
      return !this.selectedPlan || !this.selectedPatient || !this.selectedCM || !this.selectedBilling;
    } else if (!this.enrollPatientChecked) {
      return !this.firstName || !this.lastName;
    }
  }

  public handleSubmit() {

    if (this.selectedPatient && !this.selectedPatient.user.hasOwnProperty('patient_profile')) {
      let infoChanged = false;
      if (this.firstName !== this.selectedPatient.user.first_name) infoChanged = true;
      if (this.lastName !== this.selectedPatient.user.last_name) infoChanged = true;
      if (this.phoneNumber !== this.selectedPatient.user.phone) infoChanged = true;
      if (this.email !== this.selectedPatient.user.email) infoChanged = true;
      if (infoChanged) {
        this.store.User.update(this.selectedPatient.user.id, {
          phone: this.phoneNumber,
        }).subscribe(res => {
          console.log('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv');
          console.log(res);
          console.log('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^');
        })

      }
    }

    if (!this.enrollPatientChecked && this.data && this.data.potentialPatient && this.data.action === 'edit') {
       let potentialPatientSub = this.store.PotentialPatient.update(this.data.potentialPatient.id, {
        first_name: this.firstName,
        last_name: this.lastName,
        care_plan: this.selectedPlan.id,
        phone: this.phoneNumber,
        source: this.source,
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
    } else if (!this.enrollPatientChecked) {
      let potentialPatientSub = this.store.PotentialPatient.create({
        first_name: this.firstName,
        last_name: this.lastName,
        care_plan: this.selectedPlan.id,
        phone: this.phoneNumber,
        source: this.source,
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

    if (this.enrollPatientChecked && this.selectedPatient) {
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

    if (this.enrollPatientChecked && !this.selectedPatient && this.selectedFacility && this.selectedPlan && this.selectedCM) {
      this.store.AddUser.createAlt({
        email: this.email,
        first_name: this.firstName,
        last_name: this.lastName,
        password1: 'password',
        password2: 'password',
      }).subscribe(user => {
        this.store.PatientProfile.create({
          user: user.pk,
          facility: this.selectedFacility.id,
          is_active: true,
          is_invited: false,
        }).subscribe(patient => {
          this.store.CarePlan.create({
            patient: patient.id,
            plan_template: this.selectedPlan.id,
            billing_practitioner: this.selectedBilling ? this.selectedBilling.id : '',
          }).subscribe(plan => {
            this.store.CareTeamMember.create({
              employee_profile: this.selectedCM.id,
              role: this.careManagerRole.id,
              plan: plan.id,
              is_manager: true,
            }).subscribe(cm => {
              plan.careTeam = [cm];
              if (this.selectedBilling) {
                this.store.CareTeamMember.create({
                  employee_profile: this.selectedBilling.id,
                  role: this.billingPractitionerRole.id,
                  plan: plan.id,
                  is_manager: false,
                }).subscribe(bp => {
                  plan.careTeam.push(bp)
                  this.modals.close({ patient, plan });
                })
              } else {
                this.modals.close({ patient, plan })
              }
            })
          })
        })
      })
    }
  }

  public handleClose(data) {
    if (this.data.from) {

    }
    this.modals.close(null);
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

  public get filteredFacilities() {
    return this.facilities.filter(f => !f.is_affiliate);
  }

  public compareFn(c1, c2) {
    return c1 && c2 ? c1.id === c2.id : c1 === c2;
  }

  public get allPatients() {
    const arr = [
      ...this.patients,
      ...this.potentialPatients.map(p => {
        return {
          user: p
        }
      })
    ].sort((a, b) => {
      var textA = a.user.first_name.toUpperCase();
      var textB = b.user.first_name.toUpperCase();
      return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
    });
    return arr
  }
}
