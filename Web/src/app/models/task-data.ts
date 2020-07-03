import { MomentInput } from "moment";

import { ITask } from "./task";

export interface ITaskData {
  checkIns?: Array<ITask>;
  next_checkin?: MomentInput;
  tasks?: Array<ITask>;
}
