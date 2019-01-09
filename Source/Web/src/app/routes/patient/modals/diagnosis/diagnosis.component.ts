import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-diagnosis',
  templateUrl: './diagnosis.component.html',
  styleUrls: ['./diagnosis.component.scss'],
})
export class DiagnosisComponent implements OnInit {

  public data = null;

  public dropADOpen;
  public toolADOpen;
  public toolAD1Open;
  public editDiagnosisInfo;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

}
