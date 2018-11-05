import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-enrollment-required',
  templateUrl: './enrollment-required.component.html',
  styleUrls: ['./enrollment-required.component.scss'],
})
export class EnrollmentRequiredComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
