import { IHaveId } from './ihave-id';

export interface IMessage extends IHaveId {
  queue?: string;
  text?: string;
}
