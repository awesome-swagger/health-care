import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-delete-medication',
  templateUrl: './delete-medication.component.html',
  styleUrls: ['./delete-medication.component.scss'],
})
export class DeleteMedicationComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

}
