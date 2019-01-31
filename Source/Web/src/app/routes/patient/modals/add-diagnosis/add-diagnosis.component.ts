import { Component, OnInit } from '@angular/core';
import { StoreService } from '../../../../services';
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
  public employeeSearchString:string = '';
  public diagnoses = [];
  public employees = [];
  public selectedDiagnosis = null;
  public selectedEmployee = null;

  public data = null;

  constructor(
    private store: StoreService,
    private modals: ModalService,
  ) { }

  public close;

  ngOnInit() {
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
      },
      err => {},
      () => employeeSub.unsubscribe()
    )
  }

  public get searchDiagnoses() {
    if (this.diagnoses) {
      return _filter(this.diagnoses, d => d.name && d.name.toLowerCase().indexOf(this.searchString.toLowerCase()) > -1)
    }
    return null;
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

  public submit() {
    if (this.selectedDiagnosis && this.selectedEmployee) {
      this.store.PatientDiagnosis.create({
            type: "N/A",
            date_identified: moment().format('YYYY-MM-DD'),
            diagnosing_practitioner: this.employeeFullName,
            facility: null,
            patient: this.data.patientId,
            diagnosis: this.selectedDiagnosis.id
      }).subscribe(() => {})
    }
  }

}
