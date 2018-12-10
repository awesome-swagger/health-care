import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-care-plan-consent',
  templateUrl: './care-plan-consent.component.html',
  styleUrls: ['./care-plan-consent.component.scss']
})
export class CarePlanConsentComponent implements OnInit {

  constructor() { }

  public data = null;
  
  public box1;
  public box2;
  public box3;
  public box4;
  public box5;
  public box6;
  public clickCancel;
  public clickNext;

  ngOnInit() {
  }

}
