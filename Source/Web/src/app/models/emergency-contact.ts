
export interface IEmergencyContact {
  first_name?: string;
  last_name?: string;
  relationship?: string;
  phone?: string;
  /** Must be a valid email address */
  email?: string;
  is_primary?: boolean;
}
