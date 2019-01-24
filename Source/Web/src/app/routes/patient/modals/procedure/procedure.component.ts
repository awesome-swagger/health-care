import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-procedure',
  templateUrl: './procedure.component.html',
  styleUrls: ['./procedure.component.scss'],
})
export class ProcedureComponent implements OnInit {

  public data = null;

  public dropAPOpen;
  public showADDate;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

}
