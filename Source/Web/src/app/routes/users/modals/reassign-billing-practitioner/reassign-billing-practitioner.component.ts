import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';

@Component({
  selector: 'app-reassign-billing-practitioner',
  templateUrl: './reassign-billing-practitioner.component.html',
  styleUrls: ['./reassign-billing-practitioner.component.scss']
})
export class ReassignBillingPractitionerComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
  ) {}


  public facilities = [
    {
      name: 'Mountain View',
      patients: [
        {
          name: 'Cori Soderman',
        },
        {
          name: 'Theresa Beckstrom',
        },
        {
          name: 'Giovanni Manuel',
        },
        {
          name: 'Harold Taylor',
        },
      ]
    },
    {
      name: 'South Ogden Family Medicine',
      patients: [
        {
          name: 'Cori Soderman',
        },
        {
          name: 'Theresa Beckstrom',
        },
      ]
    }
  ]
  public accordianStatuses = [];

  ngOnInit() {
    this.accordianStatuses = new Array(this.facilities.length).fill(false);
  }

  public close() {
    this.modals.close(null);
  }

}
