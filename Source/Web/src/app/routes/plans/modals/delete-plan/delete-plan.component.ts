import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';

@Component({
  selector: 'app-delete-plan',
  templateUrl: './delete-plan.component.html',
  styleUrls: ['./delete-plan.component.scss']
})
export class DeletePlanComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
  ) {}

  public data = null;
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

  public ngOnInit() {
    // Get all patient's on the plan
    // group patient's by facility
    // wire up "reassign in bulk" for each facility
    // for each facility, if reassign in bulk is clicked send one post request with all patients having the same data
    // if reassign in bulk is not clicked, send a post request for each patient with different data.
    this.accordianStatuses = new Array(this.facilities.length).fill(false);
    this.data = {
      planType: "CCoM",
      planName: "Depression",
    };
  }

  public close() {
    this.modals.close(null);
  }

}
