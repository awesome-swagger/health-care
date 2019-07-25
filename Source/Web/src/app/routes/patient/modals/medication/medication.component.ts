import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';
import {
  filter as _filter
} from 'lodash';
import * as moment from 'moment';
import { P } from '@angular/core/src/render3';

@Component({
  selector: 'app-medication',
  templateUrl: './medication.component.html',
  styleUrls: ['./medication.component.scss'],
})
export class MedicationComponent implements OnInit {

  public data = null;
  public frequencyOptions: Array<any> = [
    { displayName: 'Once', value: 'once' },
    { displayName: 'Daily', value: 'daily' },
    { displayName: 'Every Other Day', value: 'every_other_day' },
    { displayName: 'Weekly', value: 'weekly' },
    { displayName: 'Weekdays', value: 'weekdays' },
    { displayName: 'Weekends', value: 'weekends' },
  ];
  public plan = null;
  public plans = [];
  public selectedPlan = null;
  public patient = null;
  public medications = [];
  public careTeamMembers = [];
  public employees = [];
  public employeeSearchString: string = '';
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
  public tooltip2Open;
  public tooltip3Open;

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.fetchMedications().then((medications: any) => {
      this.medications = medications;
    });

    let employeeSub = this.store.EmployeeProfile.readListPaged().subscribe(
      users => {
        this.employees = users;
      },
      err => { },
      () => employeeSub.unsubscribe()
    )

    if (this.data) {
      console.log('patient --- ', this.data.patient);
      this.plan = this.data.plan;
      this.plans = this.data.plans;
      this.patient = this.data.patient;
      // Get the assigned team members for this care plan
    }

    if (this.data && this.data.medication) {
      this.selectedMedication = this.data.medication.medication;
      this.datePrescribed = moment(this.data.medication.date_prescribed);
      this.doseMg = this.data.medication.dose_mg;
      this.durationDays = this.data.medication.duration_days;
      this.selectedEmployee = this.data.medication.prescribing_practitioner;
      this.employeeSearchString = this.employeeFullName;
      this.instructions = this.data.medication.instructions;

      if (this.data.medication.task) {
        const task = this.data.medication.task;
        this.appearTime = task.appear_time;
        this.dueTime = task.due_time;
        this.frequency = task.frequency;
        this.selectedPlan = this.plans.find(p => p.id === task.plan);
        this.repeatAmount = task.repeat_amount;
        this.startDay = task.start_on_day;

        if (this.repeatAmount > 0) {
          this.repeatsChoice = 'other';
        } else {
          this.repeatsChoice = 'plan_end';
        }

      }
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
      return moment(this.datePrescribed).format('MMMM D, YYYY');
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

  public saveDisabled(): boolean {
    return (!this.selectedPlan || !this.selectedMedication);
  }

  public clickDelete() {
    if (this.data.type === 'edit') {
      this.store.PatientMedication.destroy(this.data.medication.id).subscribe(res => {
        this.modal.close('delete');
      })
    }
  }

  public clickCancel() {
    this.modal.close(null);
  }

  public clickSave() {
    if (this.data.type === 'add') {
      this.store.PatientMedication.create({
        patient: this.patient.id,
        medication: this.selectedMedication.id,
        dose_mg: this.doseMg,
        date_prescribed: this.datePrescribed.format('YYYY-MM-DD'),
        duration_days: this.durationDays,
        prescribing_practitioner: this.selectedEmployee.id,
        instructions: this.instructions,
      }).subscribe(res => {

        this.store.MedicationTaskTemplate.create({
          plan: this.selectedPlan.id,
          patient_medication: res.id,
          start_on_day: this.startDay,
          frequency: this.frequency,
          repeat_amount: this.repeatsChoice === 'plan_end' ? -1 : this.repeatAmount,
          appear_time: this.appearTime,
          due_time: this.dueTime,
        }).subscribe((task: any) => {
          res.task = task;
          this.modal.close(res);
        })

      })
    }
    if (this.data.type === 'edit') {
      this.store.PatientMedication.update(this.data.medication.id, {
        patient: this.patient.id,
        medication: this.selectedMedication.id,
        dose_mg: this.doseMg,
        date_prescribed: this.datePrescribed.format('YYYY-MM-DD'),
        duration_days: this.durationDays,
        prescribing_practitioner: this.selectedEmployee.id,
        instructions: this.instructions,
      }).subscribe(res => {

        this.store.MedicationTaskTemplate.update(this.data.medication.task.id, {
          plan: this.selectedPlan.id,
          patient_medication: res.id,
          start_on_day: this.startDay,
          frequency: this.frequency,
          repeat_amount: this.repeatsChoice === 'plan_end' ? -1 : this.repeatAmount,
          appear_time: this.appearTime,
          due_time: this.dueTime,
        }).subscribe((task: any) => {
          res.task = task;
          this.modal.close(res);
        })
      })
    }


  }

  public compareFn(c1, c2) {
    return c1 && c2 ? c1.id === c2.id : c1 === c2;
  }

}
