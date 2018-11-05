import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-problem-areas',
  templateUrl: './problem-areas.component.html',
  styleUrls: ['./problem-areas.component.scss'],
})
export class ProblemAreasComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

}
