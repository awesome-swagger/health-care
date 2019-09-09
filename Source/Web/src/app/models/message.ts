import { IHaveId } from "./ihaveid";

export interface IMessage extends IHaveId {
  queue?: string;
  text?: string;
}
