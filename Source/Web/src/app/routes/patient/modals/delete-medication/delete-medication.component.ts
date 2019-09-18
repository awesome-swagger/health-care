import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';

@Component({
  selector: 'app-delete-medication',
  templateUrl: './delete-medication.component.html',
  styleUrls: ['./delete-medication.component.scss'],
})
export class DeleteMedicationComponent implements OnInit {

  public data = null;

  constructor(
    private modals: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
  }

  clickCancel() {
    this.modals.close(null);
  }

  clickSave() {
    this.store.PatientMedication.destroy(this.data.medicationId).subscribe(res => {
      this.modals.close(true);
    })
  }

}
