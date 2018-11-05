import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-plan-duration',
  templateUrl: './plan-duration.component.html',
  styleUrls: ['./plan-duration.component.scss'],
})
export class PlanDurationComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
