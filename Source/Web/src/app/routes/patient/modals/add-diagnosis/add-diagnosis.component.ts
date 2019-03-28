import { Component, OnInit } from '@angular/core';
import { StoreService, AuthService } from '../../../../services';
import { ModalService } from '../../../../modules/modals';
import {
  filter as _filter
} from 'lodash';
import * as moment from 'moment';

@Component({
  selector: 'app-add-diagnosis',
  templateUrl: './add-diagnosis.component.html',
  styleUrls: ['./add-diagnosis.component.scss']
})
export class AddDiagnosisComponent implements OnInit {

  public searchString: string = '';
  public dxSearchString:string = '';
  public employeeSearchString:string = '';
  public diagnoses = [];
  public employees = [];
  public facilities = [];
  public selectedDiagnosis = null;
  public selectedEmployee = null;
  public selectedDate = null;
  public selectedFacility = null;
  public isChronic = false;

  public data = null;

  public showDatePicker;

  constructor(
    private auth: AuthService,
    private store: StoreService,
    private modals: ModalService,
  ) { }

  ngOnInit() {
    console.log('---', this.data)
    if (this.data && this.data.patient) {
      this.selectedFacility = this.data.patient.facility;
    }
    if (this.data && this.data.diagnosis) {
      this.selectedDiagnosis = this.data.diagnosis;
      this.searchString = this.data.diagnosis.name;
      this.dxSearchString = this.data.diagnosis.dx_code;
      this.selectedDate = moment(this.data.diagnosis.patient_diagnosis.date_identified);
      this.isChronic = this.data.diagnosis.patient_diagnosis.is_chronic;
    }
    let diagnosisSub = this.store.Diagnosis.readListPaged().subscribe(
      diagnoses => {
        this.diagnoses = diagnoses;
      },
      err => {},
      () => diagnosisSub.unsubscribe()
    )

    let employeeSub = this.store.EmployeeProfile.readListPaged().subscribe(
      users => {
        this.employees = users;
        if (this.data && this.data.diagnosis) {
          const name = this.data.diagnosis.patient_diagnosis.diagnosing_practitioner.split(' ');
          this.selectedEmployee = this.employees.find(e => {
            return e.user.first_name === name[0] && e.user.last_name === name[1];
          })
          this.employeeSearchString = this.employeeFullName; 
        }
      },
      err => {},
      () => employeeSub.unsubscribe()
    )

    this.auth.organization$.subscribe(org => {
      if (!org) return;
      this.store.Organization.detailRoute('GET', org.id, 'facilities').subscribe((res:any) => {
        this.facilities = res.results;
      })
    })
  }

  public get searchDiagnoses() {
    if (this.diagnoses) {
      return _filter(this.diagnoses, d => d.name && d.name.toLowerCase().indexOf(this.searchString.toLowerCase()) > -1)
    }
    return [];
  }

  public get searchDx() {
    if (this.diagnoses) {
      return _filter(this.diagnoses, d => d.dx_code && d.dx_code.toLowerCase().indexOf(this.dxSearchString.toLowerCase()) > -1)
    }
    return [];
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

  public clearSelection() {
    this.selectedDiagnosis = null;
  }

  public clearEmployeeSelection() {
    this.selectedEmployee = null;
  }

  public get employeeFullName() {
    if (this.selectedEmployee) {
      return `${this.selectedEmployee.user.first_name} ${this.selectedEmployee.user.last_name}`;
    }
    return '';
  }

  public setSelectedDay(e) {
    this.selectedDate = e;
  }

  public close() {
    this.modals.close(null);
  }

  public submit() {
    if (this.selectedDiagnosis && this.data.type === 'add') {
      this.store.PatientDiagnosis.create({
            type: "N/A",
            date_identified: this.selectedDate.format('YYYY-MM-DD'),
            diagnosing_practitioner: this.employeeFullName,
            facility: this.selectedFacility ? this.selectedFacility.id : '',
            patient: this.data.patient.id,
            diagnosis: this.selectedDiagnosis.id,
            is_chronic: this.isChronic,
      }).subscribe((res) => {
        const diagnosis = this.data.patient.diagnosis;
        diagnosis.push(res.id)
        this.store.PatientProfile.update(this.data.patient.id, {
          diagnosis
        }).subscribe(() => {})
        this.modals.close(res);
      })
    }
    if (this.selectedDiagnosis && this.data.type === 'edit') {
      this.store.PatientDiagnosis.update(this.data.diagnosis.patient_diagnosis.id, {
        date_identified: this.selectedDate.format('YYYY-MM-DD'),
        diagnosing_practitioner: this.employeeFullName,
        facility: this.selectedFacility ? this.selectedFacility.id : '',
        diagnosis: this.selectedDiagnosis.id,
        is_chronic: this.isChronic,
      }).subscribe((res) => {
        this.modals.close(res);
      })
    }
  }

  public compareFn(c1, c2) {
    return c1 && c2 ? c1.id === c2.id : c1 === c2;
  }
}
