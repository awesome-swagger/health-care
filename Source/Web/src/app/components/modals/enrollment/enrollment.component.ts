import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-enrollment',
  templateUrl: './enrollment.component.html',
  styleUrls: ['./enrollment.component.scss'],
})
export class EnrollmentComponent implements OnInit {

  public data = null;

  public showEPStep2;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

  public phoneNum(num) {
    return `(${num.slice(0,3)})${num.slice(3,6)}-${num.slice(6,num.length)}`
  }

}
