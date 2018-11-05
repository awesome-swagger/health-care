import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-plan-expired',
  templateUrl: './plan-expired.component.html',
  styleUrls: ['./plan-expired.component.scss'],
})
export class PlanExpiredComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
