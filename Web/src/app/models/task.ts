import { MomentInput } from "moment";

export interface ITask {
  appear_datetime?: MomentInput;
  due_datetime?: MomentInput;
  id?: string;
  name?: string;
  occurrence?: string;
  patient?: {
    first_name?: string;
    id?: string;
    last_name?: string;
  };
  patientName?: string;
  state?: string;
  time?: string;
  type?: string;
}
