import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-goal-comments',
  templateUrl: './goal-comments.component.html',
  styleUrls: ['./goal-comments.component.scss'],
})
export class GoalCommentsComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

}
