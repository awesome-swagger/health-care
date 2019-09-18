import { IHaveId } from './ihave-id';

export interface ITitle extends IHaveId {
  abbreviation?: string;
  name?: string;
}
