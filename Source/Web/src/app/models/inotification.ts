import { MomentInput } from "moment";

export interface INotification {
  category?: 'unread_message' | 'flagged_patient' | 'assignment',
  created?: MomentInput,
  message?: string,
  patient?: {
    first_name?: string,
    last_name?: string
  }
}
