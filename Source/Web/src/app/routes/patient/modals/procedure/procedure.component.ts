import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';

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

  constructor(
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

  public clickCancel() {
    this.modal.close(null);
  }

  public clickSave() {
    this.modal.close({
      procedure: this.selectedProcedure.id,
      date_of_procedure: this.selectedDate.format('YYYY-MM-DD'),
      facility: this.facilityInput,
      attending_practitioner: this.practitionerInput,
    });
  }
}
