import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-plan-limit-reached',
  templateUrl: './plan-limit-reached.component.html',
  styleUrls: ['./plan-limit-reached.component.scss'],
})
export class PlanLimitReachedComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
