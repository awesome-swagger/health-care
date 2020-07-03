import { IHaveId } from './ihave-id';

export interface ISpecialty extends IHaveId {
  name?: string;
  physician_specialty?: boolean;
}
