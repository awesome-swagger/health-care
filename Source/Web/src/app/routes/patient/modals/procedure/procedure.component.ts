import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';
import { ModalService } from '../../../../modules/modals';
import { StoreService, AuthService } from '../../../../services';

@Component({
  selector: 'app-procedure',
  templateUrl: './procedure.component.html',
  styleUrls: ['./procedure.component.scss'],
})
export class ProcedureComponent implements OnInit {

  public data = null;

  public procedures = [];
  public proceduresShown = [];
  public selectedProcedure = null;
  public procedureDropOptions = {
    width: '100%',
  };
  public procedureSearchTerm = '';
  public procedureSearchOpen = false;

  public showDatePicker = false;
  public datePickerOptions = {
    'relativeTop': '48px',
  };
  public selectedDate = null;

  public practitionerInput = '';
  public facilityInput = '';

  public employees = [];
  public facilities = [];
  public employeeSearchString:string = '';
  public selectedEmployee = null;
  public facilitySearchString:string = '';
  public selectedFacility = null;

  constructor(
    private auth: AuthService,
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    this.store.Procedure.readListPaged().subscribe((procedures) => {
      this.procedures = procedures;
      this.proceduresShown = this.procedures.concat();
      if (this.data && this.data.patientProcedure) {
        this.selectedProcedure = this.data.patientProcedure.procedure;
        this.selectedDate = moment(this.data.patientProcedure.date_of_procedure);
        this.practitionerInput = this.data.patientProcedure.attending_practitioner;
        this.facilityInput = this.data.patientProcedure.facility;
      }
    });

    this.store.EmployeeProfile.readListPaged().subscribe(employees => {
      this.employees = employees;
    })
    this.auth.organization$.subscribe(org => {
      if (!org) return;
      this.store.Organization.detailRoute('GET', org.id, 'facilities').subscribe((res:any) => {
        this.facilities = res.results;
      })
    })
  }

  public filterProcedures(term) {
    this.procedureSearchTerm = term;
    this.proceduresShown = this.procedures.filter((obj) => {
      let nameMatch = obj.name.toLowerCase().indexOf(term.toLowerCase()) > -1;
      let codeMatch = obj.px_code.toLowerCase().indexOf(term.toLowerCase()) > -1;
      return nameMatch || codeMatch;
    });
  }

  public setSelectedProcedure(procedure) {
    this.selectedProcedure = procedure;
    this.procedureSearchTerm = `${procedure.name} (${procedure.px_code})`;
    this.procedureSearchOpen = false;
  }

  public clearSelectedProcedure() {
    this.selectedProcedure = null;
    this.procedureSearchTerm = '';
    this.procedureSearchOpen = true;
  }

  public setSelectedDay(e) {
    this.selectedDate = e;
  }

  public get searchEmployees() {
    if (this.employees) {
      return this.employees.filter(e => {
        const fullName = `${e.user.first_name} ${e.user.last_name}`.toLowerCase();
        return fullName.indexOf(this.employeeSearchString.toLowerCase()) > -1;
      })
    }
    return null;
  }

  public get searchFacilities() {
    if (this.facilities) {
      return this.facilities.filter(f => {
        return f.name.toLowerCase().indexOf(this.facilitySearchString.toLowerCase()) > -1;
      })
    }
    return null;
  }

  public get employeeFullName() {
    if (this.selectedEmployee) {
      return `${this.selectedEmployee.user.first_name} ${this.selectedEmployee.user.last_name}`;
    }
    return '';
  }

  public clearEmployeeSelection() {
    this.selectedEmployee = null;
  }

  public clearFacilitySelection() {
    this.selectedFacility = null;
  }


  public clickCancel() {
    this.modal.close(null);
  }

  public clickSave() {
    this.modal.close({
      procedure: this.selectedProcedure.id,
      date_of_procedure: this.selectedDate.format('YYYY-MM-DD'),
      facility: this.selectedFacility,
      attending_practitioner: this.selectedEmployee,
    });
  }
}
