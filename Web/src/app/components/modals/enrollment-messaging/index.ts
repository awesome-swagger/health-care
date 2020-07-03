import { Component, OnInit } from "@angular/core";

import { ModalService } from "../../../modules/modals";
import { Utils } from "../../../utils";

@Component({
  selector: 'app-enrollment-messaging',
  templateUrl: './index.html',
  styleUrls: ['./index.scss'],
})
export class EnrollmentMessagingComponent implements OnInit {
  public data: {
    action: () => Promise<void>,
    error: Error | string,
    message: string,
    name: string,
    success?: boolean,
  };

  constructor(
    private modals: ModalService
  ) {
    // Nothing here
  }

  public ngOnInit(): void {
    const hasAction = !Utils.isNullOrUndefined(this.data) && !Utils.isNullOrUndefined(this.data.action)
    this.data.success = hasAction;
    const action = hasAction
      ? this.data.action()
      : Promise.resolve();

    action
      .then(() => {
        this.modals.close(null);
      })
      .catch(error => {
        this.data.error = error;
        this.modals.close(null); 
      });
  }
}

export default EnrollmentMessagingComponent;
