import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-add-ct-member',
  templateUrl: './add-ct-member.component.html',
  styleUrls: ['./add-ct-member.component.scss'],
})
export class AddCTMemberComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
