import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-financial-details',
  templateUrl: './financial-details.component.html',
  styleUrls: ['./financial-details.component.scss'],
})
export class FinancialDetailsComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }

  get carePlanFull() {

    const fullPlanNames = {
      CoCM: 'Psychiatric Collaborative Care Management',
      RPM: 'Remote Patient Management',
      BHI: 'Behavioral Health Initiative',
      CCM: 'Chronic Care Management',
      CCCM: 'Complex Chronic Care Management',
      TCM: 'Transitional Care Management',
    }

    if (this.data && this.data.carePlan) {
      return fullPlanNames[this.data.carePlan] || '';
    }
  }

}
