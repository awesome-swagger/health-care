import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';
import {
  filter as _filter
} from 'lodash';
import * as moment from 'moment';

@Component({
  selector: 'app-medication',
  templateUrl: './medication.component.html',
  styleUrls: ['./medication.component.scss'],
})
export class MedicationComponent implements OnInit {

  public data = null;
  public frequencyOptions: Array<any> = [
    {displayName: 'Once', value: 'once'},
    {displayName: 'Daily', value: 'daily'},
    {displayName: 'Every Other Day', value: 'every_other_day'},
    {displayName: 'Weekly', value: 'weekly'},
    {displayName: 'Weekdays', value: 'weekdays'},
    {displayName: 'Weekends', value: 'weekends'},
  ];
  public plan = null;
  public patient = null;
  public medications = [];
  public careTeamMembers = [];
  public employees = [];
  public employeeSearchString:string = '';
  public selectedEmployee = null;
  public selectedMedication = null;
  public doseMg = 0;
  public datePrescribed = null;
  public durationDays = 0;
  public prescribingPractitioner = null;
  public instructions = '';

  public startDay = 0;
  public frequency = 'once';
  public repeatsChoice = 'plan_end';
  public repeatAmount = 1;
  public appearTime = '00:00:00';
  public dueTime = '00:00:00';

  public showDate;

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) {}

  public ngOnInit() {
    this.fetchMedications().then((medications: any) => {
      this.medications = medications;
    });

    let employeeSub = this.store.EmployeeProfile.readListPaged().subscribe(
      users => {
        this.employees = users;
      },
      err => {},
      () => employeeSub.unsubscribe()
    )

    if (this.data) {
      this.plan = this.data.plan;
      this.patient = this.data.patient;
      // Get the assigned team members for this care plan
    }
  }

  public get searchEmployees() {
    if (this.employees) {
      return _filter(this.employees, e => {
        const fullName = `${e.user.first_name} ${e.user.last_name}`.toLowerCase();
        return fullName.indexOf(this.employeeSearchString.toLowerCase()) > -1;
      })
    }
    return null;
  }

  public clearEmployeeSelection() {
    this.selectedEmployee = null;
  }

  public get employeeFullName() {
    if (this.selectedEmployee) {
      return `${this.selectedEmployee.user.first_name} ${this.selectedEmployee.user.last_name}`;
    }
  }

  public get datePrescribedFormatted() {
    if (this.datePrescribed) {
      return moment(this.datePrescribed).format('MMMM Do YYYY');
    } 
  }

  public fetchMedications() {
    let promise = new Promise((resolve, reject) => {
      let medicationsSub = this.store.Medication.readListPaged().subscribe(
        medications => {
          resolve(medications)
        },
        (err) => reject(err),
        () => medicationsSub.unsubscribe()
      )
    });
    return promise;
  }

  public saveDisabled() {
    return (
      !this.selectedMedication || !this.doseMg ||
      !this.datePrescribed || !this.durationDays ||
      !this.selectedEmployee || !this.datePrescribed);
  }

  public clickCancel() {
    this.modal.close(null);
  }

  public clickSave() {
    this.store.PatientMedication.create({
      patient: this.patient.id,
      medication: this.selectedMedication,
      dose_mg: this.doseMg,
      date_prescribed: this.datePrescribed.format('YYYY-MM-DD'),
      duration_days: this.durationDays,
      prescribing_practitioner: this.selectedEmployee.id,
    }).subscribe(res => {
      this.modal.close(res);
    })
  }
}
