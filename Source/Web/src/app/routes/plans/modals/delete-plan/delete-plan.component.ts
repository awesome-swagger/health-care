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

  ngOnInit() {
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


