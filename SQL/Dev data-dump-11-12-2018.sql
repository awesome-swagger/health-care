--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account_emailaddress; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.account_emailaddress (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    verified boolean NOT NULL,
    "primary" boolean NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.account_emailaddress OWNER TO care_adopt_backend;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.account_emailaddress_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_emailaddress_id_seq OWNER TO care_adopt_backend;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.account_emailaddress_id_seq OWNED BY public.account_emailaddress.id;


--
-- Name: account_emailconfirmation; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.account_emailconfirmation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sent timestamp with time zone,
    key character varying(64) NOT NULL,
    email_address_id integer NOT NULL
);


ALTER TABLE public.account_emailconfirmation OWNER TO care_adopt_backend;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.account_emailconfirmation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_emailconfirmation_id_seq OWNER TO care_adopt_backend;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.account_emailconfirmation_id_seq OWNED BY public.account_emailconfirmation.id;


--
-- Name: accounts_emailuser; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.accounts_emailuser (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    id uuid NOT NULL,
    email character varying(254) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    image character varying(100),
    preferred_name character varying(30) NOT NULL,
    gender character varying(1),
    birthdate date,
    phone character varying(16) NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    validated_at timestamp with time zone,
    validation_key uuid,
    reset_key uuid,
    is_developer boolean NOT NULL,
    time_zone character varying(128) NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.accounts_emailuser OWNER TO care_adopt_backend;

--
-- Name: accounts_emailuser_groups; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.accounts_emailuser_groups (
    id integer NOT NULL,
    emailuser_id uuid NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.accounts_emailuser_groups OWNER TO care_adopt_backend;

--
-- Name: accounts_emailuser_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.accounts_emailuser_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_emailuser_groups_id_seq OWNER TO care_adopt_backend;

--
-- Name: accounts_emailuser_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.accounts_emailuser_groups_id_seq OWNED BY public.accounts_emailuser_groups.id;


--
-- Name: accounts_emailuser_user_permissions; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.accounts_emailuser_user_permissions (
    id integer NOT NULL,
    emailuser_id uuid NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.accounts_emailuser_user_permissions OWNER TO care_adopt_backend;

--
-- Name: accounts_emailuser_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.accounts_emailuser_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_emailuser_user_permissions_id_seq OWNER TO care_adopt_backend;

--
-- Name: accounts_emailuser_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.accounts_emailuser_user_permissions_id_seq OWNED BY public.accounts_emailuser_user_permissions.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO care_adopt_backend;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO care_adopt_backend;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO care_adopt_backend;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO care_adopt_backend;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO care_adopt_backend;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO care_adopt_backend;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO care_adopt_backend;

--
-- Name: core_diagnosis; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_diagnosis (
    id uuid NOT NULL,
    name character varying(140) NOT NULL,
    dx_code character varying(100)
);


ALTER TABLE public.core_diagnosis OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_employeeprofile (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    npi_code character varying(100),
    specialty_id uuid,
    title_id uuid,
    user_id uuid NOT NULL,
    status character varying(20) NOT NULL
);


ALTER TABLE public.core_employeeprofile OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_facilities; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_employeeprofile_facilities (
    id integer NOT NULL,
    employeeprofile_id uuid NOT NULL,
    facility_id uuid NOT NULL
);


ALTER TABLE public.core_employeeprofile_facilities OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_facilities_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.core_employeeprofile_facilities_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_employeeprofile_facilities_id_seq OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_facilities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.core_employeeprofile_facilities_id_seq OWNED BY public.core_employeeprofile_facilities.id;


--
-- Name: core_employeeprofile_facilities_managed; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_employeeprofile_facilities_managed (
    id integer NOT NULL,
    employeeprofile_id uuid NOT NULL,
    facility_id uuid NOT NULL
);


ALTER TABLE public.core_employeeprofile_facilities_managed OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_facilities_managed_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.core_employeeprofile_facilities_managed_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_employeeprofile_facilities_managed_id_seq OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_facilities_managed_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.core_employeeprofile_facilities_managed_id_seq OWNED BY public.core_employeeprofile_facilities_managed.id;


--
-- Name: core_employeeprofile_organizations; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_employeeprofile_organizations (
    id integer NOT NULL,
    employeeprofile_id uuid NOT NULL,
    organization_id uuid NOT NULL
);


ALTER TABLE public.core_employeeprofile_organizations OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_organizations_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.core_employeeprofile_organizations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_employeeprofile_organizations_id_seq OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_organizations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.core_employeeprofile_organizations_id_seq OWNED BY public.core_employeeprofile_organizations.id;


--
-- Name: core_employeeprofile_organizations_managed; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_employeeprofile_organizations_managed (
    id integer NOT NULL,
    employeeprofile_id uuid NOT NULL,
    organization_id uuid NOT NULL
);


ALTER TABLE public.core_employeeprofile_organizations_managed OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_organizations_managed_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.core_employeeprofile_organizations_managed_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_employeeprofile_organizations_managed_id_seq OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_organizations_managed_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.core_employeeprofile_organizations_managed_id_seq OWNED BY public.core_employeeprofile_organizations_managed.id;


--
-- Name: core_employeeprofile_roles; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_employeeprofile_roles (
    id integer NOT NULL,
    employeeprofile_id uuid NOT NULL,
    providerrole_id uuid NOT NULL
);


ALTER TABLE public.core_employeeprofile_roles OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.core_employeeprofile_roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_employeeprofile_roles_id_seq OWNER TO care_adopt_backend;

--
-- Name: core_employeeprofile_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.core_employeeprofile_roles_id_seq OWNED BY public.core_employeeprofile_roles.id;


--
-- Name: core_facility; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_facility (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    addr_street character varying(255),
    addr_suite character varying(35),
    addr_city character varying(255),
    addr_state character varying(255),
    addr_zip character varying(15),
    name character varying(120) NOT NULL,
    is_affiliate boolean NOT NULL,
    parent_company character varying(120),
    organization_id uuid NOT NULL
);


ALTER TABLE public.core_facility OWNER TO care_adopt_backend;

--
-- Name: core_invitedemailtemplate; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_invitedemailtemplate (
    id uuid NOT NULL,
    subject character varying(140) NOT NULL,
    message character varying(500) NOT NULL,
    is_default boolean NOT NULL
);


ALTER TABLE public.core_invitedemailtemplate OWNER TO care_adopt_backend;

--
-- Name: core_medication; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_medication (
    id uuid NOT NULL,
    name character varying(140) NOT NULL,
    rx_code character varying(100)
);


ALTER TABLE public.core_medication OWNER TO care_adopt_backend;

--
-- Name: core_organization; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_organization (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    addr_street character varying(255),
    addr_suite character varying(35),
    addr_city character varying(255),
    addr_state character varying(255),
    addr_zip character varying(15),
    name character varying(120) NOT NULL
);


ALTER TABLE public.core_organization OWNER TO care_adopt_backend;

--
-- Name: core_procedure; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_procedure (
    id uuid NOT NULL,
    name character varying(140) NOT NULL,
    px_code character varying(100)
);


ALTER TABLE public.core_procedure OWNER TO care_adopt_backend;

--
-- Name: core_providerrole; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_providerrole (
    id uuid NOT NULL,
    name character varying(35) NOT NULL
);


ALTER TABLE public.core_providerrole OWNER TO care_adopt_backend;

--
-- Name: core_providerspecialty; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_providerspecialty (
    id uuid NOT NULL,
    name character varying(35) NOT NULL,
    physician_specialty boolean NOT NULL
);


ALTER TABLE public.core_providerspecialty OWNER TO care_adopt_backend;

--
-- Name: core_providertitle; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_providertitle (
    id uuid NOT NULL,
    name character varying(35) NOT NULL,
    abbreviation character varying(10) NOT NULL
);


ALTER TABLE public.core_providertitle OWNER TO care_adopt_backend;

--
-- Name: core_symptom; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.core_symptom (
    id uuid NOT NULL,
    name character varying(140) NOT NULL,
    worst_label character varying(40) NOT NULL,
    best_label character varying(40) NOT NULL
);


ALTER TABLE public.core_symptom OWNER TO care_adopt_backend;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id uuid NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO care_adopt_backend;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO care_adopt_backend;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO care_adopt_backend;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO care_adopt_backend;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO care_adopt_backend;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO care_adopt_backend;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO care_adopt_backend;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO care_adopt_backend;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO care_adopt_backend;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: patients_patientdiagnosis; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.patients_patientdiagnosis (
    id uuid NOT NULL,
    type character varying(20) NOT NULL,
    date_identified date,
    diagnosing_practitioner character varying(140),
    facility character varying(140),
    diagnosis_id uuid NOT NULL,
    patient_id uuid NOT NULL
);


ALTER TABLE public.patients_patientdiagnosis OWNER TO care_adopt_backend;

--
-- Name: patients_patientmedication; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.patients_patientmedication (
    id uuid NOT NULL,
    dose_mg integer NOT NULL,
    date_prescribed date NOT NULL,
    duration_days integer NOT NULL,
    instructions character varying(480),
    medication_id uuid NOT NULL,
    patient_id uuid NOT NULL,
    prescribing_practitioner_id uuid
);


ALTER TABLE public.patients_patientmedication OWNER TO care_adopt_backend;

--
-- Name: patients_patientprocedure; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.patients_patientprocedure (
    id uuid NOT NULL,
    date_of_procedure date,
    attending_practitioner character varying(140),
    facility character varying(140),
    patient_id uuid NOT NULL,
    procedure_id uuid NOT NULL
);


ALTER TABLE public.patients_patientprocedure OWNER TO care_adopt_backend;

--
-- Name: patients_patientprofile; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.patients_patientprofile (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    facility_id uuid NOT NULL,
    user_id uuid NOT NULL,
    emr_code character varying(100),
    message_for_day_id uuid,
    is_active boolean NOT NULL,
    is_invited boolean NOT NULL,
    last_app_use timestamp with time zone NOT NULL
);


ALTER TABLE public.patients_patientprofile OWNER TO care_adopt_backend;

--
-- Name: patients_patientprofile_diagnosis; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.patients_patientprofile_diagnosis (
    id integer NOT NULL,
    patientprofile_id uuid NOT NULL,
    patientdiagnosis_id uuid NOT NULL
);


ALTER TABLE public.patients_patientprofile_diagnosis OWNER TO care_adopt_backend;

--
-- Name: patients_patientprofile_diagnosis_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.patients_patientprofile_diagnosis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.patients_patientprofile_diagnosis_id_seq OWNER TO care_adopt_backend;

--
-- Name: patients_patientprofile_diagnosis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.patients_patientprofile_diagnosis_id_seq OWNED BY public.patients_patientprofile_diagnosis.id;


--
-- Name: patients_patientverificationcode; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.patients_patientverificationcode (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    code character varying(6) NOT NULL,
    patient_id uuid NOT NULL
);


ALTER TABLE public.patients_patientverificationcode OWNER TO care_adopt_backend;

--
-- Name: patients_potentialpatient; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.patients_potentialpatient (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    care_plan character varying(64) NOT NULL,
    phone character varying(16) NOT NULL,
    patient_profile_id uuid
);


ALTER TABLE public.patients_potentialpatient OWNER TO care_adopt_backend;

--
-- Name: patients_potentialpatient_facility; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.patients_potentialpatient_facility (
    id integer NOT NULL,
    potentialpatient_id uuid NOT NULL,
    facility_id uuid NOT NULL
);


ALTER TABLE public.patients_potentialpatient_facility OWNER TO care_adopt_backend;

--
-- Name: patients_potentialpatient_facility_id_seq; Type: SEQUENCE; Schema: public; Owner: care_adopt_backend
--

CREATE SEQUENCE public.patients_potentialpatient_facility_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.patients_potentialpatient_facility_id_seq OWNER TO care_adopt_backend;

--
-- Name: patients_potentialpatient_facility_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: care_adopt_backend
--

ALTER SEQUENCE public.patients_potentialpatient_facility_id_seq OWNED BY public.patients_potentialpatient_facility.id;


--
-- Name: patients_problemarea; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.patients_problemarea (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    date_identified date,
    name character varying(140) NOT NULL,
    description character varying(512),
    identified_by_id uuid,
    patient_id uuid NOT NULL
);


ALTER TABLE public.patients_problemarea OWNER TO care_adopt_backend;

--
-- Name: patients_reminderemail; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.patients_reminderemail (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    subject character varying(140) NOT NULL,
    message character varying(500) NOT NULL,
    patient_id uuid NOT NULL
);


ALTER TABLE public.patients_reminderemail OWNER TO care_adopt_backend;

--
-- Name: plans_careplan; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.plans_careplan (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    patient_id uuid NOT NULL,
    plan_template_id uuid NOT NULL
);


ALTER TABLE public.plans_careplan OWNER TO care_adopt_backend;

--
-- Name: plans_careplantemplate; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.plans_careplantemplate (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    name character varying(120) NOT NULL,
    type character varying(10) NOT NULL,
    duration_weeks integer NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.plans_careplantemplate OWNER TO care_adopt_backend;

--
-- Name: plans_careteammember; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.plans_careteammember (
    id uuid NOT NULL,
    employee_profile_id uuid NOT NULL,
    plan_id uuid NOT NULL,
    role_id uuid NOT NULL,
    is_manager boolean NOT NULL
);


ALTER TABLE public.plans_careteammember OWNER TO care_adopt_backend;

--
-- Name: plans_goal; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.plans_goal (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    goal_template_id uuid NOT NULL,
    plan_id uuid NOT NULL,
    start_on_datetime timestamp with time zone NOT NULL
);


ALTER TABLE public.plans_goal OWNER TO care_adopt_backend;

--
-- Name: plans_goalcomment; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.plans_goalcomment (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    content text NOT NULL,
    goal_id uuid NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.plans_goalcomment OWNER TO care_adopt_backend;

--
-- Name: plans_goalprogress; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.plans_goalprogress (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    rating integer NOT NULL,
    goal_id uuid NOT NULL
);


ALTER TABLE public.plans_goalprogress OWNER TO care_adopt_backend;

--
-- Name: plans_goaltemplate; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.plans_goaltemplate (
    id uuid NOT NULL,
    name character varying(140) NOT NULL,
    description character varying(240) NOT NULL,
    focus character varying(140) NOT NULL,
    start_on_day integer NOT NULL,
    duration_weeks integer NOT NULL,
    plan_template_id uuid NOT NULL
);


ALTER TABLE public.plans_goaltemplate OWNER TO care_adopt_backend;

--
-- Name: plans_infomessage; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.plans_infomessage (
    id uuid NOT NULL,
    text character varying(512),
    queue_id uuid NOT NULL
);


ALTER TABLE public.plans_infomessage OWNER TO care_adopt_backend;

--
-- Name: plans_infomessagequeue; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.plans_infomessagequeue (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    name character varying(120) NOT NULL,
    type character varying(40) NOT NULL,
    plan_template_id uuid NOT NULL
);


ALTER TABLE public.plans_infomessagequeue OWNER TO care_adopt_backend;

--
-- Name: plans_planconsent; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.plans_planconsent (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    verbal_consent boolean NOT NULL,
    discussed_co_pay boolean NOT NULL,
    seen_within_year boolean NOT NULL,
    will_use_mobile_app boolean NOT NULL,
    will_interact_with_team boolean NOT NULL,
    will_complete_tasks boolean NOT NULL,
    plan_id uuid NOT NULL
);


ALTER TABLE public.plans_planconsent OWNER TO care_adopt_backend;

--
-- Name: tasks_assessmentquestion; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_assessmentquestion (
    id uuid NOT NULL,
    prompt character varying(240) NOT NULL,
    worst_label character varying(40) NOT NULL,
    best_label character varying(40) NOT NULL,
    assessment_task_template_id uuid NOT NULL
);


ALTER TABLE public.tasks_assessmentquestion OWNER TO care_adopt_backend;

--
-- Name: tasks_assessmentresponse; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_assessmentresponse (
    id uuid NOT NULL,
    rating integer NOT NULL,
    assessment_question_id uuid NOT NULL,
    assessment_task_id uuid NOT NULL
);


ALTER TABLE public.tasks_assessmentresponse OWNER TO care_adopt_backend;

--
-- Name: tasks_assessmenttask; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_assessmenttask (
    id uuid NOT NULL,
    appear_datetime timestamp with time zone NOT NULL,
    due_datetime timestamp with time zone NOT NULL,
    comments character varying(1024),
    plan_id uuid NOT NULL,
    assessment_task_template_id uuid NOT NULL,
    is_complete boolean NOT NULL
);


ALTER TABLE public.tasks_assessmenttask OWNER TO care_adopt_backend;

--
-- Name: tasks_assessmenttasktemplate; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_assessmenttasktemplate (
    id uuid NOT NULL,
    start_on_day integer NOT NULL,
    frequency character varying(20) NOT NULL,
    repeat_amount integer NOT NULL,
    appear_time time without time zone NOT NULL,
    due_time time without time zone NOT NULL,
    tracks_outcome boolean NOT NULL,
    tracks_satisfaction boolean NOT NULL,
    plan_template_id uuid NOT NULL,
    name character varying(120) NOT NULL
);


ALTER TABLE public.tasks_assessmenttasktemplate OWNER TO care_adopt_backend;

--
-- Name: tasks_medicationtask; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_medicationtask (
    id uuid NOT NULL,
    appear_datetime timestamp with time zone NOT NULL,
    due_datetime timestamp with time zone NOT NULL,
    status character varying(12) NOT NULL,
    medication_task_template_id uuid NOT NULL
);


ALTER TABLE public.tasks_medicationtask OWNER TO care_adopt_backend;

--
-- Name: tasks_medicationtasktemplate; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_medicationtasktemplate (
    id uuid NOT NULL,
    start_on_day integer NOT NULL,
    frequency character varying(20) NOT NULL,
    repeat_amount integer NOT NULL,
    appear_time time without time zone NOT NULL,
    due_time time without time zone NOT NULL,
    patient_medication_id uuid NOT NULL,
    plan_id uuid NOT NULL
);


ALTER TABLE public.tasks_medicationtasktemplate OWNER TO care_adopt_backend;

--
-- Name: tasks_patienttask; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_patienttask (
    id uuid NOT NULL,
    appear_datetime timestamp with time zone NOT NULL,
    due_datetime timestamp with time zone NOT NULL,
    status character varying(12) NOT NULL,
    patient_task_template_id uuid NOT NULL,
    plan_id uuid NOT NULL
);


ALTER TABLE public.tasks_patienttask OWNER TO care_adopt_backend;

--
-- Name: tasks_patienttasktemplate; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_patienttasktemplate (
    id uuid NOT NULL,
    start_on_day integer NOT NULL,
    frequency character varying(20) NOT NULL,
    repeat_amount integer NOT NULL,
    appear_time time without time zone NOT NULL,
    due_time time without time zone NOT NULL,
    name character varying(140) NOT NULL,
    plan_template_id uuid NOT NULL
);


ALTER TABLE public.tasks_patienttasktemplate OWNER TO care_adopt_backend;

--
-- Name: tasks_symptomrating; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_symptomrating (
    id uuid NOT NULL,
    rating integer NOT NULL,
    symptom_id uuid NOT NULL,
    symptom_task_id uuid NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL
);


ALTER TABLE public.tasks_symptomrating OWNER TO care_adopt_backend;

--
-- Name: tasks_symptomtask; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_symptomtask (
    id uuid NOT NULL,
    appear_datetime timestamp with time zone NOT NULL,
    due_datetime timestamp with time zone NOT NULL,
    comments character varying(1024),
    plan_id uuid NOT NULL,
    symptom_task_template_id uuid NOT NULL,
    is_complete boolean NOT NULL
);


ALTER TABLE public.tasks_symptomtask OWNER TO care_adopt_backend;

--
-- Name: tasks_symptomtasktemplate; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_symptomtasktemplate (
    id uuid NOT NULL,
    start_on_day integer NOT NULL,
    frequency character varying(20) NOT NULL,
    repeat_amount integer NOT NULL,
    appear_time time without time zone NOT NULL,
    due_time time without time zone NOT NULL,
    plan_template_id uuid NOT NULL
);


ALTER TABLE public.tasks_symptomtasktemplate OWNER TO care_adopt_backend;

--
-- Name: tasks_teamtask; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_teamtask (
    id uuid NOT NULL,
    appear_datetime timestamp with time zone NOT NULL,
    due_datetime timestamp with time zone NOT NULL,
    plan_id uuid NOT NULL,
    team_task_template_id uuid NOT NULL,
    status character varying(12) NOT NULL
);


ALTER TABLE public.tasks_teamtask OWNER TO care_adopt_backend;

--
-- Name: tasks_teamtasktemplate; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_teamtasktemplate (
    id uuid NOT NULL,
    start_on_day integer NOT NULL,
    frequency character varying(20) NOT NULL,
    repeat_amount integer NOT NULL,
    appear_time time without time zone NOT NULL,
    due_time time without time zone NOT NULL,
    name character varying(140) NOT NULL,
    is_manager_task boolean NOT NULL,
    category character varying(120) NOT NULL,
    plan_template_id uuid NOT NULL,
    role_id uuid
);


ALTER TABLE public.tasks_teamtasktemplate OWNER TO care_adopt_backend;

--
-- Name: tasks_vitalquestion; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_vitalquestion (
    id uuid NOT NULL,
    prompt character varying(255) NOT NULL,
    answer_type character varying(128) NOT NULL,
    vital_task_template_id uuid NOT NULL
);


ALTER TABLE public.tasks_vitalquestion OWNER TO care_adopt_backend;

--
-- Name: tasks_vitalresponse; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_vitalresponse (
    id uuid NOT NULL,
    answer_boolean boolean,
    answer_time time without time zone,
    answer_float double precision,
    answer_integer integer,
    answer_scale integer,
    answer_string character varying(255) NOT NULL,
    question_id uuid NOT NULL,
    vital_task_id uuid NOT NULL
);


ALTER TABLE public.tasks_vitalresponse OWNER TO care_adopt_backend;

--
-- Name: tasks_vitaltask; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_vitaltask (
    id uuid NOT NULL,
    appear_datetime timestamp with time zone NOT NULL,
    due_datetime timestamp with time zone NOT NULL,
    is_complete boolean NOT NULL,
    plan_id uuid NOT NULL,
    vital_task_template_id uuid NOT NULL
);


ALTER TABLE public.tasks_vitaltask OWNER TO care_adopt_backend;

--
-- Name: tasks_vitaltasktemplate; Type: TABLE; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE TABLE public.tasks_vitaltasktemplate (
    id uuid NOT NULL,
    start_on_day integer NOT NULL,
    frequency character varying(20) NOT NULL,
    repeat_amount integer NOT NULL,
    appear_time time without time zone NOT NULL,
    due_time time without time zone NOT NULL,
    name character varying(254) NOT NULL,
    plan_template_id uuid NOT NULL
);


ALTER TABLE public.tasks_vitaltasktemplate OWNER TO care_adopt_backend;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.account_emailaddress ALTER COLUMN id SET DEFAULT nextval('public.account_emailaddress_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.account_emailconfirmation ALTER COLUMN id SET DEFAULT nextval('public.account_emailconfirmation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.accounts_emailuser_groups ALTER COLUMN id SET DEFAULT nextval('public.accounts_emailuser_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.accounts_emailuser_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.accounts_emailuser_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_facilities ALTER COLUMN id SET DEFAULT nextval('public.core_employeeprofile_facilities_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_facilities_managed ALTER COLUMN id SET DEFAULT nextval('public.core_employeeprofile_facilities_managed_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_organizations ALTER COLUMN id SET DEFAULT nextval('public.core_employeeprofile_organizations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_organizations_managed ALTER COLUMN id SET DEFAULT nextval('public.core_employeeprofile_organizations_managed_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_roles ALTER COLUMN id SET DEFAULT nextval('public.core_employeeprofile_roles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientprofile_diagnosis ALTER COLUMN id SET DEFAULT nextval('public.patients_patientprofile_diagnosis_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_potentialpatient_facility ALTER COLUMN id SET DEFAULT nextval('public.patients_potentialpatient_facility_id_seq'::regclass);


--
-- Data for Name: account_emailaddress; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.account_emailaddress (id, email, verified, "primary", user_id) FROM stdin;
\.


--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.account_emailaddress_id_seq', 1, false);


--
-- Data for Name: account_emailconfirmation; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.account_emailconfirmation (id, created, sent, key, email_address_id) FROM stdin;
\.


--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.account_emailconfirmation_id_seq', 1, false);


--
-- Data for Name: accounts_emailuser; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.accounts_emailuser (password, last_login, is_superuser, id, email, first_name, last_name, image, preferred_name, gender, birthdate, phone, date_joined, validated_at, validation_key, reset_key, is_developer, time_zone, is_active) FROM stdin;
pbkdf2_sha256$100000$1lBI66hrQadO$k71OTfMsonvjoHzX3MpCHf20SGwnY5iw1kAkANbb4G0=	2018-09-25 06:36:27.332784+00	t	6998f5f2-4396-4f95-9281-1365144c80ef	pat.keeps.looking.up@gmail.com	Pat	Tan			\N	\N		2018-09-25 02:54:33.066968+00	2018-09-25 02:54:52+00	\N	\N	f	America/Denver	t
pbkdf2_sha256$100000$NoTQb1nD8gbD$uwT7e51XFMYI6LNhQD+Bt+X5O0ycHLHZoRz1aI3DUKE=	2018-09-14 00:27:29.008712+00	t	5794fb47-d466-4686-b467-fb6c0124a712	ronil.rufo@gmail.com	Ronil	Rufo			\N	\N		2018-09-14 00:24:18.694808+00	2018-09-14 00:24:33+00	\N	\N	f	America/Denver	t
pbkdf2_sha256$100000$yhTtFearXlJx$s7Q32plkKpnJNjW5R9yiihkuz1zZMeZW0vldi8r+prs=	2018-10-03 23:49:18.916798+00	t	4d58f161-27f3-4fbe-91b5-930c6b4e2952	jlewis.code@gmail.com	Joe	Lewis			\N	\N		2018-09-14 23:30:44.867868+00	2018-09-14 23:30:56+00	\N	\N	f	America/Denver	t
pbkdf2_sha256$100000$7ahG59rUFwdo$wbmMyeCIs6Z9atPTR57Ms7qVSk4BfWwHNs0NCfjLu+E=	\N	t	ff414879-bfed-4b4a-8fa7-eab316944611	bryce.bartel@careadopt.com	Bryce	Bartel			\N	\N		2018-07-23 15:32:31.203489+00	2018-07-23 15:33:40+00	\N	\N	f	America/Denver	t
pbkdf2_sha256$100000$hDge9pwUjKX8$I3QUGjsKUbBRGosf1h25JuXDo/SZUo0Mo0yldxTdrfQ=	\N	t	96925dc0-3d85-4963-a547-ff1d08473a3d	nbills@startstudio.com	Namon	Bills			\N	\N		2018-07-23 15:33:58.961758+00	2018-07-23 15:34:03+00	\N	\N	f	America/Denver	t
pbkdf2_sha256$100000$L66C531jyPxi$VFDGYMU1U2M+TdOfbEyhnij+7pihW0JDjheaXt+HDJo=	\N	t	deb62432-8faa-4f80-b78e-e48faf6ec4c7	kcole@startstudio.com	Kacey	Cole			\N	\N		2018-09-15 05:00:52.398489+00	2018-09-15 05:01:23+00	\N	\N	f	America/Denver	t
pbkdf2_sha256$100000$72npMARIosZ0$zXsEakYUeq/ojgLE+XqurSXZWK8plI9tKQYNUCBLAXw=	2018-08-13 16:07:42.720062+00	t	bda0b489-b99e-45f6-93e1-27dfc6942da9	jwright@mindfiretechnology.com	Justin	Wright			\N	\N		2018-08-13 16:01:17.376565+00	\N	d0e833cc-76e0-4e3c-920b-ca13a3abd9c2	\N	t	America/Denver	t
pbkdf2_sha256$100000$tQxubBo12qkL$yvlW6k4NZuWd5ChbE/giTKQvzsbdeArvvWYiTslfya4=	2018-08-20 16:40:37.994953+00	t	881665e9-625a-4fa3-9d32-a670fdf04b4a	ESevy@MindfireTechnology.com	Evan	Sevy			m	\N		2018-07-27 16:13:47.941314+00	2018-07-27 18:50:08+00	\N	\N	t	America/Denver	t
pbkdf2_sha256$100000$Fw2ymB4vU7Pt$3GxamkOV2Aq0Ewq3QxzyrOeYLAqHi+OFlI+nFesjloE=	2018-09-17 20:23:29.19708+00	t	bd86f4b9-951a-467c-98dd-f9fb535d255a	tyler.delange@healthlogicsoftware.com	Tyler	Delange			\N	\N		2018-07-23 15:33:01.079992+00	2018-07-23 15:33:03+00	\N	\N	f	America/Denver	t
pbkdf2_sha256$100000$HplCbZI46PHo$KzGqHhPx8aoaPU3Eivo93FGljru34zwmhVoQe7Ji7p4=	2018-07-26 00:24:55.303676+00	t	a9112a07-3151-4f61-ac6d-c1e7d2becfdf	nate@mindfiretechnology.com	Nate	Mindfire			\N	\N		2018-07-23 15:33:22.920932+00	2018-07-23 15:33:26+00	\N	\N	f	America/Denver	t
pbkdf2_sha256$100000$bMZSJpMzLrfp$fwVhvp5A3V2slrO/yw+Wc57mgMuv4Ncb+ZMiparrEUo=	2018-11-06 23:20:16.469199+00	t	024978c2-f9f8-4ec6-8773-5efaf8f13eea	dbeus@mindfiretechnology.com	Johnny	Appleseed			\N	\N		2018-07-24 15:11:47.303157+00	2018-07-27 18:52:26+00	\N	\N	t	America/Denver	t
pbkdf2_sha256$100000$udKas9eZMVa8$b6mkAeSRQIK3L+5S9/utNp1oIYRKqfOthwfA6uk0uo4=	2018-11-11 05:49:05.283834+00	t	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8	jprice@startstudio.com	Jordan	Price			\N	\N		2018-07-23 15:27:51.871637+00	2018-07-23 15:37:02+00	\N	\N	f	America/Denver	t
pbkdf2_sha256$100000$HfJkB3I55aax$NBPpvpAYN2iicNTbHeeJ5EYc+keTHb5+Jc1PyQx8tJ8=	2018-10-16 23:23:19.957586+00	t	e5169647-5801-40ff-aa23-147ea5c58c60	jgunderson@startstudio.com	Jordan	Gunderson			\N	\N		2018-07-23 15:34:16.530277+00	2018-07-23 15:34:20+00	\N	\N	f	America/Denver	t
pbkdf2_sha256$100000$Oqr1MqthY8Bk$xbr1BBJQSqMQCIzvnioXeMHvVkhuCUs3ktIDckHFtUM=	2018-10-24 19:43:43.899045+00	f	86b92518-9c2a-4ca8-a471-2860473c4b9e	jprice@izeni.com	Jordan	Price		John	\N	\N		2018-10-17 06:37:26.888444+00	2018-10-17 06:37:26+00	c55b8917-bcbf-4e98-865d-700a3236b5f3	\N	f	America/Denver	t
pbkdf2_sha256$100000$vWgzki3YWAgt$7f6Uq0sWPPHkEkr4j5FARFZVpn70Id1V2lUYLzGGW5M=	2018-10-24 19:44:58.891209+00	f	668ab8f8-b0e9-4788-9abf-89d997f290b8	patient@test.com	Patient	Test			\N	\N		2018-07-23 15:38:58.718617+00	2018-07-23 15:39:20+00	\N	\N	f	America/Denver	t
\.


--
-- Data for Name: accounts_emailuser_groups; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.accounts_emailuser_groups (id, emailuser_id, group_id) FROM stdin;
\.


--
-- Name: accounts_emailuser_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.accounts_emailuser_groups_id_seq', 1, false);


--
-- Data for Name: accounts_emailuser_user_permissions; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.accounts_emailuser_user_permissions (id, emailuser_id, permission_id) FROM stdin;
\.


--
-- Name: accounts_emailuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.accounts_emailuser_user_permissions_id_seq', 1, false);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add content type	4	add_contenttype
11	Can change content type	4	change_contenttype
12	Can delete content type	4	delete_contenttype
13	Can add session	5	add_session
14	Can change session	5	change_session
15	Can delete session	5	delete_session
16	Can add Token	6	add_token
17	Can change Token	6	change_token
18	Can delete Token	6	delete_token
19	Can add user	7	add_emailuser
20	Can change user	7	change_emailuser
21	Can delete user	7	delete_emailuser
22	Can add provider specialty	8	add_providerspecialty
23	Can change provider specialty	8	change_providerspecialty
24	Can delete provider specialty	8	delete_providerspecialty
25	Can add provider title	9	add_providertitle
26	Can change provider title	9	change_providertitle
27	Can delete provider title	9	delete_providertitle
28	Can add employee profile	10	add_employeeprofile
29	Can change employee profile	10	change_employeeprofile
30	Can delete employee profile	10	delete_employeeprofile
31	Can add diagnosis	11	add_diagnosis
32	Can change diagnosis	11	change_diagnosis
33	Can delete diagnosis	11	delete_diagnosis
34	Can add organization	12	add_organization
35	Can change organization	12	change_organization
36	Can delete organization	12	delete_organization
37	Can add procedure	13	add_procedure
38	Can change procedure	13	change_procedure
39	Can delete procedure	13	delete_procedure
40	Can add medication	14	add_medication
41	Can change medication	14	change_medication
42	Can delete medication	14	delete_medication
43	Can add facility	15	add_facility
44	Can change facility	15	change_facility
45	Can delete facility	15	delete_facility
46	Can add provider role	16	add_providerrole
47	Can change provider role	16	change_providerrole
48	Can delete provider role	16	delete_providerrole
49	Can add patient diagnosis	17	add_patientdiagnosis
50	Can change patient diagnosis	17	change_patientdiagnosis
51	Can delete patient diagnosis	17	delete_patientdiagnosis
52	Can add patient profile	18	add_patientprofile
53	Can change patient profile	18	change_patientprofile
54	Can delete patient profile	18	delete_patientprofile
55	Can add problem area	19	add_problemarea
56	Can change problem area	19	change_problemarea
57	Can delete problem area	19	delete_problemarea
58	Can add patient procedure	20	add_patientprocedure
59	Can change patient procedure	20	change_patientprocedure
60	Can delete patient procedure	20	delete_patientprocedure
61	Can add care plan instance	21	add_careplaninstance
62	Can change care plan instance	21	change_careplaninstance
63	Can delete care plan instance	21	delete_careplaninstance
64	Can add plan consent	22	add_planconsent
65	Can change plan consent	22	change_planconsent
66	Can delete plan consent	22	delete_planconsent
67	Can add goal	23	add_goal
68	Can change goal	23	change_goal
69	Can delete goal	23	delete_goal
70	Can add care plan template	24	add_careplantemplate
71	Can change care plan template	24	change_careplantemplate
72	Can delete care plan template	24	delete_careplantemplate
73	Can add team task	25	add_teamtask
74	Can change team task	25	change_teamtask
75	Can delete team task	25	delete_teamtask
76	Can add patient medication	26	add_patientmedication
77	Can change patient medication	26	change_patientmedication
78	Can delete patient medication	26	delete_patientmedication
79	Can add patient task	27	add_patienttask
80	Can change patient task	27	change_patienttask
81	Can delete patient task	27	delete_patienttask
82	Can add stream message	28	add_streammessage
83	Can change stream message	28	change_streammessage
84	Can delete stream message	28	delete_streammessage
85	Can add message stream	29	add_messagestream
86	Can change message stream	29	change_messagestream
87	Can delete message stream	29	delete_messagestream
88	Can add info message	30	add_infomessage
89	Can change info message	30	change_infomessage
90	Can delete info message	30	delete_infomessage
91	Can add patient task instance	31	add_patienttaskinstance
92	Can change patient task instance	31	change_patienttaskinstance
93	Can delete patient task instance	31	delete_patienttaskinstance
94	Can add team task template	32	add_teamtasktemplate
95	Can change team task template	32	change_teamtasktemplate
96	Can delete team task template	32	delete_teamtasktemplate
97	Can add goal template	33	add_goaltemplate
98	Can change goal template	33	change_goaltemplate
99	Can delete goal template	33	delete_goaltemplate
100	Can add patient task template	34	add_patienttasktemplate
101	Can change patient task template	34	change_patienttasktemplate
102	Can delete patient task template	34	delete_patienttasktemplate
103	Can add care team member	35	add_careteammember
104	Can change care team member	35	change_careteammember
105	Can delete care team member	35	delete_careteammember
106	Can add info message queue	36	add_infomessagequeue
107	Can change info message queue	36	change_infomessagequeue
108	Can delete info message queue	36	delete_infomessagequeue
109	Can add medication task instance	37	add_medicationtaskinstance
110	Can change medication task instance	37	change_medicationtaskinstance
111	Can delete medication task instance	37	delete_medicationtaskinstance
112	Can add medication task template	38	add_medicationtasktemplate
113	Can change medication task template	38	change_medicationtasktemplate
114	Can delete medication task template	38	delete_medicationtasktemplate
115	Can add symptom	39	add_symptom
116	Can change symptom	39	change_symptom
117	Can delete symptom	39	delete_symptom
118	Can add assessment task template	40	add_assessmenttasktemplate
119	Can change assessment task template	40	change_assessmenttasktemplate
120	Can delete assessment task template	40	delete_assessmenttasktemplate
121	Can add medication task template	41	add_medicationtasktemplate
122	Can change medication task template	41	change_medicationtasktemplate
123	Can delete medication task template	41	delete_medicationtasktemplate
124	Can add symptom task template	42	add_symptomtasktemplate
125	Can change symptom task template	42	change_symptomtasktemplate
126	Can delete symptom task template	42	delete_symptomtasktemplate
127	Can add assessment task instance	43	add_assessmenttaskinstance
128	Can change assessment task instance	43	change_assessmenttaskinstance
129	Can delete assessment task instance	43	delete_assessmenttaskinstance
130	Can add assessment question	44	add_assessmentquestion
131	Can change assessment question	44	change_assessmentquestion
132	Can delete assessment question	44	delete_assessmentquestion
133	Can add team task instance	45	add_teamtaskinstance
134	Can change team task instance	45	change_teamtaskinstance
135	Can delete team task instance	45	delete_teamtaskinstance
136	Can add medication task instance	46	add_medicationtaskinstance
137	Can change medication task instance	46	change_medicationtaskinstance
138	Can delete medication task instance	46	delete_medicationtaskinstance
139	Can add patient task instance	47	add_patienttaskinstance
140	Can change patient task instance	47	change_patienttaskinstance
141	Can delete patient task instance	47	delete_patienttaskinstance
142	Can add assessment response	48	add_assessmentresponse
143	Can change assessment response	48	change_assessmentresponse
144	Can delete assessment response	48	delete_assessmentresponse
145	Can add symptom rating	49	add_symptomrating
146	Can change symptom rating	49	change_symptomrating
147	Can delete symptom rating	49	delete_symptomrating
148	Can add team task template	50	add_teamtasktemplate
149	Can change team task template	50	change_teamtasktemplate
150	Can delete team task template	50	delete_teamtasktemplate
151	Can add patient task template	51	add_patienttasktemplate
152	Can change patient task template	51	change_patienttasktemplate
153	Can delete patient task template	51	delete_patienttasktemplate
154	Can add symptom task instance	52	add_symptomtaskinstance
155	Can change symptom task instance	52	change_symptomtaskinstance
156	Can delete symptom task instance	52	delete_symptomtaskinstance
157	Can add care plan	21	add_careplan
158	Can change care plan	21	change_careplan
159	Can delete care plan	21	delete_careplan
160	Can add symptom task	52	add_symptomtask
161	Can change symptom task	52	change_symptomtask
162	Can delete symptom task	52	delete_symptomtask
163	Can add assessment task	43	add_assessmenttask
164	Can change assessment task	43	change_assessmenttask
165	Can delete assessment task	43	delete_assessmenttask
166	Can add patient task	47	add_patienttask
167	Can change patient task	47	change_patienttask
168	Can delete patient task	47	delete_patienttask
169	Can add team task	45	add_teamtask
170	Can change team task	45	change_teamtask
171	Can delete team task	45	delete_teamtask
172	Can add medication task	46	add_medicationtask
173	Can change medication task	46	change_medicationtask
174	Can delete medication task	46	delete_medicationtask
175	Can add Goal Progress	53	add_goalprogress
176	Can change Goal Progress	53	change_goalprogress
177	Can delete Goal Progress	53	delete_goalprogress
178	Can add Goal Comment	54	add_goalcomment
179	Can change Goal Comment	54	change_goalcomment
180	Can delete Goal Comment	54	delete_goalcomment
181	Can add Vital Task Template	55	add_vitaltasktemplate
182	Can change Vital Task Template	55	change_vitaltasktemplate
183	Can delete Vital Task Template	55	delete_vitaltasktemplate
184	Can add vital task	56	add_vitaltask
185	Can change vital task	56	change_vitaltask
186	Can delete vital task	56	delete_vitaltask
187	Can add vital question	57	add_vitalquestion
188	Can change vital question	57	change_vitalquestion
189	Can delete vital question	57	delete_vitalquestion
190	Can add vital response	58	add_vitalresponse
191	Can change vital response	58	change_vitalresponse
192	Can delete vital response	58	delete_vitalresponse
193	Can add site	59	add_site
194	Can change site	59	change_site
195	Can delete site	59	delete_site
196	Can add email address	60	add_emailaddress
197	Can change email address	60	change_emailaddress
198	Can delete email address	60	delete_emailaddress
199	Can add email confirmation	61	add_emailconfirmation
200	Can change email confirmation	61	change_emailconfirmation
201	Can delete email confirmation	61	delete_emailconfirmation
202	Can add invited email template	62	add_invitedemailtemplate
203	Can change invited email template	62	change_invitedemailtemplate
204	Can delete invited email template	62	delete_invitedemailtemplate
205	Can add reminder email	63	add_reminderemail
206	Can change reminder email	63	change_reminderemail
207	Can delete reminder email	63	delete_reminderemail
208	Can add Patient Verification Code	64	add_patientverificationcode
209	Can change Patient Verification Code	64	change_patientverificationcode
210	Can delete Patient Verification Code	64	delete_patientverificationcode
211	Can add Potential Patient	65	add_potentialpatient
212	Can change Potential Patient	65	change_potentialpatient
213	Can delete Potential Patient	65	delete_potentialpatient
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 213, true);


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
3418be61de8df273dce940171fcacc177120d6d8	2018-07-23 15:44:29.225156+00	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
70eb762554af260c507c36b9c4ef8f644ece51c9	2018-08-07 15:33:08.967239+00	024978c2-f9f8-4ec6-8773-5efaf8f13eea
2d7ac1834003afa448185157296ba688a1cc1e8e	2018-08-13 16:15:05.895452+00	881665e9-625a-4fa3-9d32-a670fdf04b4a
df7d541ea112d10d57585522d41b4c601c352c0f	2018-08-14 18:51:50.976669+00	96925dc0-3d85-4963-a547-ff1d08473a3d
1a2a9acb795dbea06611d73f0afce01a38b880bc	2018-08-15 00:23:40.915556+00	ff414879-bfed-4b4a-8fa7-eab316944611
84e8dfdec101a932a9898e141b85af15aba07e6e	2018-09-05 21:11:31.414662+00	bd86f4b9-951a-467c-98dd-f9fb535d255a
f9ba6d2a325bb023c4b91b6238355d3ef01e05af	2018-09-12 00:47:28.302455+00	668ab8f8-b0e9-4788-9abf-89d997f290b8
3b5ff9d40481e42a1cf22ad01bb3a2966aa5f11c	2018-09-14 23:36:00.499183+00	4d58f161-27f3-4fbe-91b5-930c6b4e2952
1d96e5891c00a2ac61c590e3157ee9307faef3dd	2018-09-25 06:11:24.163676+00	6998f5f2-4396-4f95-9281-1365144c80ef
e04b784a5c941f24011ea81c111619abee2c512e	2018-10-17 06:40:57.221007+00	86b92518-9c2a-4ca8-a471-2860473c4b9e
\.


--
-- Data for Name: core_diagnosis; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_diagnosis (id, name, dx_code) FROM stdin;
ece37c05-48f9-45d2-8e81-c533deb924b5	Cancer	1
98ffe758-e7d0-4539-a213-e4781e6218ee	Freckles	Fr
\.


--
-- Data for Name: core_employeeprofile; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_employeeprofile (created, modified, id, npi_code, specialty_id, title_id, user_id, status) FROM stdin;
2018-08-14 18:49:10.694295+00	2018-08-14 18:49:26.567122+00	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	\N	51420140-c878-4aa6-81b8-e83e04d2e11e	583a434e-fd28-4270-b604-f571130096cb	96925dc0-3d85-4963-a547-ff1d08473a3d	invited
2018-08-15 00:23:02.448083+00	2018-08-15 19:46:30.450823+00	13571e24-bfb8-4729-949a-f617bcf2f70a	\N	51420140-c878-4aa6-81b8-e83e04d2e11e	583a434e-fd28-4270-b604-f571130096cb	ff414879-bfed-4b4a-8fa7-eab316944611	active
2018-09-05 20:43:32.394865+00	2018-09-05 20:43:32.394883+00	01cbc1e6-4582-4e31-a38b-20a8605e835c	\N	51420140-c878-4aa6-81b8-e83e04d2e11e	583a434e-fd28-4270-b604-f571130096cb	bd86f4b9-951a-467c-98dd-f9fb535d255a	invited
2018-09-12 03:18:55.788646+00	2018-09-12 03:18:55.788667+00	f56fe653-5b3c-493d-86f5-ec7dbd932dde	\N	51420140-c878-4aa6-81b8-e83e04d2e11e	583a434e-fd28-4270-b604-f571130096cb	e5169647-5801-40ff-aa23-147ea5c58c60	invited
2018-09-14 23:31:50.664136+00	2018-09-14 23:31:50.664156+00	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	\N	51420140-c878-4aa6-81b8-e83e04d2e11e	583a434e-fd28-4270-b604-f571130096cb	4d58f161-27f3-4fbe-91b5-930c6b4e2952	invited
2018-09-15 05:01:53.180261+00	2018-09-15 05:01:53.180294+00	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	\N	51420140-c878-4aa6-81b8-e83e04d2e11e	5535b8e2-9bd1-48da-ade7-5f7d5e76eb98	deb62432-8faa-4f80-b78e-e48faf6ec4c7	invited
2018-09-25 02:58:11.55735+00	2018-09-25 02:58:11.557368+00	de594b37-6201-4469-9a33-81fd03e5ad65	\N	51420140-c878-4aa6-81b8-e83e04d2e11e	5535b8e2-9bd1-48da-ade7-5f7d5e76eb98	6998f5f2-4396-4f95-9281-1365144c80ef	invited
2018-07-23 15:36:51.126742+00	2018-10-08 20:29:59.458028+00	68523cec-50cb-4510-9508-99983fb0c8de	111111	51420140-c878-4aa6-81b8-e83e04d2e11e	5535b8e2-9bd1-48da-ade7-5f7d5e76eb98	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8	invited
\.


--
-- Data for Name: core_employeeprofile_facilities; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_employeeprofile_facilities (id, employeeprofile_id, facility_id) FROM stdin;
1	68523cec-50cb-4510-9508-99983fb0c8de	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
2	68523cec-50cb-4510-9508-99983fb0c8de	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
5	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
6	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	07aa1282-18a2-4e36-bba9-3d5581402d6d
7	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
8	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
9	13571e24-bfb8-4729-949a-f617bcf2f70a	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
10	13571e24-bfb8-4729-949a-f617bcf2f70a	07aa1282-18a2-4e36-bba9-3d5581402d6d
11	13571e24-bfb8-4729-949a-f617bcf2f70a	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
12	13571e24-bfb8-4729-949a-f617bcf2f70a	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
13	01cbc1e6-4582-4e31-a38b-20a8605e835c	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
14	01cbc1e6-4582-4e31-a38b-20a8605e835c	07aa1282-18a2-4e36-bba9-3d5581402d6d
15	01cbc1e6-4582-4e31-a38b-20a8605e835c	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
16	01cbc1e6-4582-4e31-a38b-20a8605e835c	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
17	f56fe653-5b3c-493d-86f5-ec7dbd932dde	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
18	f56fe653-5b3c-493d-86f5-ec7dbd932dde	07aa1282-18a2-4e36-bba9-3d5581402d6d
19	f56fe653-5b3c-493d-86f5-ec7dbd932dde	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
20	f56fe653-5b3c-493d-86f5-ec7dbd932dde	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
21	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
22	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	07aa1282-18a2-4e36-bba9-3d5581402d6d
23	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
24	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
25	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
26	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	07aa1282-18a2-4e36-bba9-3d5581402d6d
27	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
28	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
29	de594b37-6201-4469-9a33-81fd03e5ad65	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
30	de594b37-6201-4469-9a33-81fd03e5ad65	07aa1282-18a2-4e36-bba9-3d5581402d6d
31	de594b37-6201-4469-9a33-81fd03e5ad65	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
32	de594b37-6201-4469-9a33-81fd03e5ad65	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
\.


--
-- Name: core_employeeprofile_facilities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.core_employeeprofile_facilities_id_seq', 32, true);


--
-- Data for Name: core_employeeprofile_facilities_managed; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_employeeprofile_facilities_managed (id, employeeprofile_id, facility_id) FROM stdin;
1	68523cec-50cb-4510-9508-99983fb0c8de	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
2	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
3	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	07aa1282-18a2-4e36-bba9-3d5581402d6d
4	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
5	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
6	13571e24-bfb8-4729-949a-f617bcf2f70a	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
7	13571e24-bfb8-4729-949a-f617bcf2f70a	07aa1282-18a2-4e36-bba9-3d5581402d6d
8	13571e24-bfb8-4729-949a-f617bcf2f70a	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
9	13571e24-bfb8-4729-949a-f617bcf2f70a	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
10	01cbc1e6-4582-4e31-a38b-20a8605e835c	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
11	01cbc1e6-4582-4e31-a38b-20a8605e835c	07aa1282-18a2-4e36-bba9-3d5581402d6d
12	01cbc1e6-4582-4e31-a38b-20a8605e835c	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
13	01cbc1e6-4582-4e31-a38b-20a8605e835c	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
14	f56fe653-5b3c-493d-86f5-ec7dbd932dde	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
15	f56fe653-5b3c-493d-86f5-ec7dbd932dde	07aa1282-18a2-4e36-bba9-3d5581402d6d
16	f56fe653-5b3c-493d-86f5-ec7dbd932dde	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
17	f56fe653-5b3c-493d-86f5-ec7dbd932dde	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
18	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
19	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	07aa1282-18a2-4e36-bba9-3d5581402d6d
20	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
21	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
22	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
23	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	07aa1282-18a2-4e36-bba9-3d5581402d6d
24	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
25	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
26	de594b37-6201-4469-9a33-81fd03e5ad65	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3
27	de594b37-6201-4469-9a33-81fd03e5ad65	07aa1282-18a2-4e36-bba9-3d5581402d6d
28	de594b37-6201-4469-9a33-81fd03e5ad65	dcc71bd8-31cf-4e98-a26c-cac02021f5f6
29	de594b37-6201-4469-9a33-81fd03e5ad65	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889
\.


--
-- Name: core_employeeprofile_facilities_managed_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.core_employeeprofile_facilities_managed_id_seq', 29, true);


--
-- Data for Name: core_employeeprofile_organizations; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_employeeprofile_organizations (id, employeeprofile_id, organization_id) FROM stdin;
1	68523cec-50cb-4510-9508-99983fb0c8de	d855296f-a03e-4b6e-add1-f66cabacef1f
2	68523cec-50cb-4510-9508-99983fb0c8de	37478b1f-d050-4fd2-9035-2038da3c7d35
3	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	d855296f-a03e-4b6e-add1-f66cabacef1f
4	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	37478b1f-d050-4fd2-9035-2038da3c7d35
5	13571e24-bfb8-4729-949a-f617bcf2f70a	d855296f-a03e-4b6e-add1-f66cabacef1f
6	01cbc1e6-4582-4e31-a38b-20a8605e835c	d855296f-a03e-4b6e-add1-f66cabacef1f
7	01cbc1e6-4582-4e31-a38b-20a8605e835c	37478b1f-d050-4fd2-9035-2038da3c7d35
8	f56fe653-5b3c-493d-86f5-ec7dbd932dde	d855296f-a03e-4b6e-add1-f66cabacef1f
9	f56fe653-5b3c-493d-86f5-ec7dbd932dde	37478b1f-d050-4fd2-9035-2038da3c7d35
10	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	d855296f-a03e-4b6e-add1-f66cabacef1f
11	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	37478b1f-d050-4fd2-9035-2038da3c7d35
12	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	d855296f-a03e-4b6e-add1-f66cabacef1f
13	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	37478b1f-d050-4fd2-9035-2038da3c7d35
14	de594b37-6201-4469-9a33-81fd03e5ad65	d855296f-a03e-4b6e-add1-f66cabacef1f
15	de594b37-6201-4469-9a33-81fd03e5ad65	37478b1f-d050-4fd2-9035-2038da3c7d35
\.


--
-- Name: core_employeeprofile_organizations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.core_employeeprofile_organizations_id_seq', 15, true);


--
-- Data for Name: core_employeeprofile_organizations_managed; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_employeeprofile_organizations_managed (id, employeeprofile_id, organization_id) FROM stdin;
1	68523cec-50cb-4510-9508-99983fb0c8de	d855296f-a03e-4b6e-add1-f66cabacef1f
2	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	d855296f-a03e-4b6e-add1-f66cabacef1f
3	13571e24-bfb8-4729-949a-f617bcf2f70a	d855296f-a03e-4b6e-add1-f66cabacef1f
4	01cbc1e6-4582-4e31-a38b-20a8605e835c	d855296f-a03e-4b6e-add1-f66cabacef1f
5	01cbc1e6-4582-4e31-a38b-20a8605e835c	37478b1f-d050-4fd2-9035-2038da3c7d35
6	f56fe653-5b3c-493d-86f5-ec7dbd932dde	d855296f-a03e-4b6e-add1-f66cabacef1f
7	f56fe653-5b3c-493d-86f5-ec7dbd932dde	37478b1f-d050-4fd2-9035-2038da3c7d35
8	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	d855296f-a03e-4b6e-add1-f66cabacef1f
9	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	37478b1f-d050-4fd2-9035-2038da3c7d35
10	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	d855296f-a03e-4b6e-add1-f66cabacef1f
11	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	37478b1f-d050-4fd2-9035-2038da3c7d35
12	de594b37-6201-4469-9a33-81fd03e5ad65	d855296f-a03e-4b6e-add1-f66cabacef1f
13	de594b37-6201-4469-9a33-81fd03e5ad65	37478b1f-d050-4fd2-9035-2038da3c7d35
\.


--
-- Name: core_employeeprofile_organizations_managed_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.core_employeeprofile_organizations_managed_id_seq', 13, true);


--
-- Data for Name: core_employeeprofile_roles; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_employeeprofile_roles (id, employeeprofile_id, providerrole_id) FROM stdin;
1	68523cec-50cb-4510-9508-99983fb0c8de	f706665f-c518-4bd5-ad31-68c3d40fad8a
2	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	f706665f-c518-4bd5-ad31-68c3d40fad8a
3	13571e24-bfb8-4729-949a-f617bcf2f70a	f706665f-c518-4bd5-ad31-68c3d40fad8a
4	01cbc1e6-4582-4e31-a38b-20a8605e835c	e78afb29-e874-424e-92e7-6245f8190beb
5	01cbc1e6-4582-4e31-a38b-20a8605e835c	f706665f-c518-4bd5-ad31-68c3d40fad8a
6	f56fe653-5b3c-493d-86f5-ec7dbd932dde	e78afb29-e874-424e-92e7-6245f8190beb
7	f56fe653-5b3c-493d-86f5-ec7dbd932dde	f706665f-c518-4bd5-ad31-68c3d40fad8a
8	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	e78afb29-e874-424e-92e7-6245f8190beb
9	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	f706665f-c518-4bd5-ad31-68c3d40fad8a
10	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	e78afb29-e874-424e-92e7-6245f8190beb
11	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	f706665f-c518-4bd5-ad31-68c3d40fad8a
12	de594b37-6201-4469-9a33-81fd03e5ad65	e78afb29-e874-424e-92e7-6245f8190beb
13	de594b37-6201-4469-9a33-81fd03e5ad65	f706665f-c518-4bd5-ad31-68c3d40fad8a
\.


--
-- Name: core_employeeprofile_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.core_employeeprofile_roles_id_seq', 13, true);


--
-- Data for Name: core_facility; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_facility (created, modified, id, addr_street, addr_suite, addr_city, addr_state, addr_zip, name, is_affiliate, parent_company, organization_id) FROM stdin;
2018-07-23 15:35:46.657891+00	2018-07-23 15:35:46.657911+00	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3	1159 East 12th Street	\N	Odgen	UT	84404	Canyon View	f	\N	d855296f-a03e-4b6e-add1-f66cabacef1f
2018-07-23 15:52:07.209988+00	2018-07-23 15:52:07.210008+00	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889	3225W Gordon Ave	Suite 1	Layton	Ut	84041	Davis Family Physicians	f	\N	d855296f-a03e-4b6e-add1-f66cabacef1f
2018-07-23 15:53:09.802876+00	2018-07-23 15:53:09.802897+00	07aa1282-18a2-4e36-bba9-3d5581402d6d	3485 West 5200 South	\N	Roy	UT	84067	Grand View	f	\N	d855296f-a03e-4b6e-add1-f66cabacef1f
2018-07-23 15:53:31.012862+00	2018-07-23 15:53:31.012883+00	dcc71bd8-31cf-4e98-a26c-cac02021f5f6	934S Main St.	#6	Layton	UT	84041	Davis Behavioral Health	t	\N	d855296f-a03e-4b6e-add1-f66cabacef1f
\.


--
-- Data for Name: core_invitedemailtemplate; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_invitedemailtemplate (id, subject, message, is_default) FROM stdin;
\.


--
-- Data for Name: core_medication; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_medication (id, name, rx_code) FROM stdin;
3ee1039a-0dd6-4dcc-b31b-cf3dc61de361	Amoxicillin	1
4c4ba942-8979-40b4-8252-7e2da81d7e8c	Erythromycin	2
\.


--
-- Data for Name: core_organization; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_organization (created, modified, id, addr_street, addr_suite, addr_city, addr_state, addr_zip, name) FROM stdin;
2018-07-23 15:35:18.915659+00	2018-07-23 15:35:18.915681+00	d855296f-a03e-4b6e-add1-f66cabacef1f	1491 East Ridgeline Dr	\N	Odgen	UT	84404	Ogden Clinic
2018-07-26 03:31:42.874638+00	2018-07-26 03:31:42.874657+00	37478b1f-d050-4fd2-9035-2038da3c7d35	1159 East 12th Street	\N	Odgen	UT	84404	Ogden Family Medicine
\.


--
-- Data for Name: core_procedure; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_procedure (id, name, px_code) FROM stdin;
54d366af-9ae6-45fe-acac-a3f5a45b9bf0	Apendectimy	1
\.


--
-- Data for Name: core_providerrole; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_providerrole (id, name) FROM stdin;
f706665f-c518-4bd5-ad31-68c3d40fad8a	Care Manager
e78afb29-e874-424e-92e7-6245f8190beb	Medical Doctor
\.


--
-- Data for Name: core_providerspecialty; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_providerspecialty (id, name, physician_specialty) FROM stdin;
51420140-c878-4aa6-81b8-e83e04d2e11e	Family Medicine	f
\.


--
-- Data for Name: core_providertitle; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_providertitle (id, name, abbreviation) FROM stdin;
5535b8e2-9bd1-48da-ade7-5f7d5e76eb98	Care Coordinator	CC
583a434e-fd28-4270-b604-f571130096cb	Medical Doctor	MD
\.


--
-- Data for Name: core_symptom; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.core_symptom (id, name, worst_label, best_label) FROM stdin;
a344d800-55b3-4853-83cb-1c814a75a9c2	Fatigue	Very Fatigued	No Fatigue
0c3bf862-ca7c-42d6-9d42-6b7995919973	Pain	Very Painful	No Pain
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2018-07-23 15:32:31.373425+00	ff414879-bfed-4b4a-8fa7-eab316944611	bryce.bartel@careadopt.com	1	[{"added": {}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
2	2018-07-23 15:33:01.185934+00	bd86f4b9-951a-467c-98dd-f9fb535d255a	tyler.delange@healthlogicsoftware.com	1	[{"added": {}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
3	2018-07-23 15:33:06.764766+00	bd86f4b9-951a-467c-98dd-f9fb535d255a	tyler.delange@healthlogicsoftware.com	2	[{"changed": {"fields": ["validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
4	2018-07-23 15:33:23.02719+00	a9112a07-3151-4f61-ac6d-c1e7d2becfdf	nate@mindfiretechnology.com	1	[{"added": {}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
5	2018-07-23 15:33:31.693577+00	a9112a07-3151-4f61-ac6d-c1e7d2becfdf	nate@mindfiretechnology.com	2	[{"changed": {"fields": ["validation_key", "validated_at", "is_superuser"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
6	2018-07-23 15:33:35.676432+00	bd86f4b9-951a-467c-98dd-f9fb535d255a	tyler.delange@healthlogicsoftware.com	2	[{"changed": {"fields": ["is_superuser"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
7	2018-07-23 15:33:41.952859+00	ff414879-bfed-4b4a-8fa7-eab316944611	bryce.bartel@careadopt.com	2	[{"changed": {"fields": ["validation_key", "validated_at", "is_superuser"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
8	2018-07-23 15:33:59.066588+00	96925dc0-3d85-4963-a547-ff1d08473a3d	nbills@startstudio.com	1	[{"added": {}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
9	2018-07-23 15:34:07.171999+00	96925dc0-3d85-4963-a547-ff1d08473a3d	nbills@startstudio.com	2	[{"changed": {"fields": ["validation_key", "validated_at", "is_superuser"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
10	2018-07-23 15:34:16.639876+00	e5169647-5801-40ff-aa23-147ea5c58c60	jgunderson@startstudio.com	1	[{"added": {}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
11	2018-07-23 15:34:21.547906+00	e5169647-5801-40ff-aa23-147ea5c58c60	jgunderson@startstudio.com	2	[{"changed": {"fields": ["validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
12	2018-07-23 15:34:26.796997+00	e5169647-5801-40ff-aa23-147ea5c58c60	jgunderson@startstudio.com	2	[{"changed": {"fields": ["is_superuser"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
13	2018-07-23 15:35:18.916379+00	d855296f-a03e-4b6e-add1-f66cabacef1f	Ogden Clinic	1	[{"added": {}}]	12	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
14	2018-07-23 15:35:46.658712+00	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3	Ogden Clinic: Canyon View	1	[{"added": {}}]	15	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
15	2018-07-23 15:36:19.229949+00	5535b8e2-9bd1-48da-ade7-5f7d5e76eb98	Care Coordinator	1	[{"added": {}}]	9	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
16	2018-07-23 15:36:39.949816+00	f706665f-c518-4bd5-ad31-68c3d40fad8a	Care Manager	1	[{"added": {}}]	16	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
17	2018-07-23 15:36:49.484102+00	51420140-c878-4aa6-81b8-e83e04d2e11e	Family Medicine	1	[{"added": {}}]	8	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
18	2018-07-23 15:36:51.141525+00	68523cec-50cb-4510-9508-99983fb0c8de	 , CC	1	[{"added": {}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
19	2018-07-23 15:37:10.792096+00	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8	jprice@startstudio.com	2	[{"changed": {"fields": ["first_name", "last_name", "validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
20	2018-07-23 15:37:18.71579+00	ff414879-bfed-4b4a-8fa7-eab316944611	bryce.bartel@careadopt.com	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
21	2018-07-23 15:37:26.415928+00	e5169647-5801-40ff-aa23-147ea5c58c60	jgunderson@startstudio.com	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
22	2018-07-23 15:37:34.741723+00	a9112a07-3151-4f61-ac6d-c1e7d2becfdf	nate@mindfiretechnology.com	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
23	2018-07-23 15:37:40.598684+00	96925dc0-3d85-4963-a547-ff1d08473a3d	nbills@startstudio.com	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
24	2018-07-23 15:37:45.994916+00	bd86f4b9-951a-467c-98dd-f9fb535d255a	tyler.delange@healthlogicsoftware.com	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
25	2018-07-23 15:38:58.8421+00	668ab8f8-b0e9-4788-9abf-89d997f290b8	patient@test.com	1	[{"added": {}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
26	2018-07-23 15:39:06.681251+00	78d5472b-32d4-4b15-8dd1-f14a65070da4	 	1	[{"added": {}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
27	2018-07-23 15:39:23.713826+00	668ab8f8-b0e9-4788-9abf-89d997f290b8	patient@test.com	2	[{"changed": {"fields": ["first_name", "last_name", "validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
28	2018-07-23 15:52:07.210619+00	fa42899f-9d3c-4fb9-b2b7-6163b2fdf889	Ogden Clinic: Davis Family Physicians	1	[{"added": {}}]	15	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
29	2018-07-23 15:53:09.803503+00	07aa1282-18a2-4e36-bba9-3d5581402d6d	Ogden Clinic: Grand View	1	[{"added": {}}]	15	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
30	2018-07-23 15:53:31.013471+00	dcc71bd8-31cf-4e98-a26c-cac02021f5f6	Ogden Clinic: Davis Behavioral Health	1	[{"added": {}}]	15	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
31	2018-07-23 15:53:49.001793+00	68523cec-50cb-4510-9508-99983fb0c8de	Jordan Price, CC	2	[{"changed": {"fields": ["facilities", "facilities_managed"]}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
32	2018-07-24 15:11:47.428996+00	024978c2-f9f8-4ec6-8773-5efaf8f13eea	dbeus@mindfiretechnology.com	1	[{"added": {}}]	7	a9112a07-3151-4f61-ac6d-c1e7d2becfdf
33	2018-07-24 15:12:09.995991+00	024978c2-f9f8-4ec6-8773-5efaf8f13eea	dbeus@mindfiretechnology.com	2	[{"changed": {"fields": ["is_developer", "is_superuser"]}}]	7	a9112a07-3151-4f61-ac6d-c1e7d2becfdf
34	2018-07-24 15:12:26.480965+00	024978c2-f9f8-4ec6-8773-5efaf8f13eea	dbeus@mindfiretechnology.com	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	7	a9112a07-3151-4f61-ac6d-c1e7d2becfdf
35	2018-07-26 03:31:42.875195+00	37478b1f-d050-4fd2-9035-2038da3c7d35	Ogden Family Medicine	1	[{"added": {}}]	12	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
36	2018-07-26 03:32:03.306807+00	68523cec-50cb-4510-9508-99983fb0c8de	Jordan Price, CC	2	[{"changed": {"fields": ["organizations", "organizations_managed"]}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
37	2018-07-27 16:13:48.069675+00	881665e9-625a-4fa3-9d32-a670fdf04b4a	ESevy@MindfireTechnology.com	1	[{"added": {}}]	7	a9112a07-3151-4f61-ac6d-c1e7d2becfdf
38	2018-07-27 16:15:14.094664+00	881665e9-625a-4fa3-9d32-a670fdf04b4a	ESevy@MindfireTechnology.com	2	[{"changed": {"fields": ["first_name", "last_name", "gender", "is_developer", "is_superuser"]}}]	7	a9112a07-3151-4f61-ac6d-c1e7d2becfdf
39	2018-07-27 16:15:17.920277+00	881665e9-625a-4fa3-9d32-a670fdf04b4a	ESevy@MindfireTechnology.com	2	[]	7	a9112a07-3151-4f61-ac6d-c1e7d2becfdf
40	2018-07-27 16:17:48.331535+00	83437bc8-ac13-47f7-a1fd-727fc4d40b8d	Evan Sevy	1	[{"added": {}}]	18	a9112a07-3151-4f61-ac6d-c1e7d2becfdf
41	2018-07-27 18:50:11.579533+00	881665e9-625a-4fa3-9d32-a670fdf04b4a	ESevy@MindfireTechnology.com	2	[{"changed": {"fields": ["validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
42	2018-07-27 18:52:29.458052+00	024978c2-f9f8-4ec6-8773-5efaf8f13eea	dbeus@mindfiretechnology.com	2	[{"changed": {"fields": ["validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
43	2018-08-06 17:55:06.921754+00	6b35be7c-427f-40bd-977e-468746e946f2	Daniel Beus	1	[{"added": {}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
44	2018-08-06 18:02:08.442426+00	6b35be7c-427f-40bd-977e-468746e946f2	Daniel Beus	2	[]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
45	2018-08-07 21:06:17.886704+00	1e986c82-0fcc-494f-b1a5-b9d78be4964c	Daniel Beus: Cancer	2	[{"changed": {"fields": ["type"]}}]	17	024978c2-f9f8-4ec6-8773-5efaf8f13eea
46	2018-08-13 15:45:24.637958+00	6eb761bc-a4cb-4615-8612-778d96446fb7	jwright@mindfiretechnology.com	1	[{"added": {}}]	7	024978c2-f9f8-4ec6-8773-5efaf8f13eea
47	2018-08-13 15:45:45.650609+00	6eb761bc-a4cb-4615-8612-778d96446fb7	jwright@mindfiretechnology.com	2	[{"changed": {"fields": ["first_name", "last_name", "validated_at", "is_developer"]}}]	7	024978c2-f9f8-4ec6-8773-5efaf8f13eea
48	2018-08-13 15:58:39.348825+00	6eb761bc-a4cb-4615-8612-778d96446fb7	jwright@mindfiretechnology.com	2	[{"changed": {"fields": ["is_superuser"]}}]	7	024978c2-f9f8-4ec6-8773-5efaf8f13eea
49	2018-08-13 16:00:49.374701+00	6eb761bc-a4cb-4615-8612-778d96446fb7	jwright@mindfiretechnology.com	3		7	024978c2-f9f8-4ec6-8773-5efaf8f13eea
50	2018-08-13 16:01:17.498144+00	bda0b489-b99e-45f6-93e1-27dfc6942da9	jwright@mindfiretechnology.com	1	[{"added": {}}]	7	024978c2-f9f8-4ec6-8773-5efaf8f13eea
51	2018-08-13 16:07:43.116123+00	bda0b489-b99e-45f6-93e1-27dfc6942da9	jwright@mindfiretechnology.com	2	[{"changed": {"fields": ["is_developer"]}}]	7	024978c2-f9f8-4ec6-8773-5efaf8f13eea
52	2018-08-13 16:08:01.649677+00	bda0b489-b99e-45f6-93e1-27dfc6942da9	jwright@mindfiretechnology.com	2	[{"changed": {"fields": ["first_name", "last_name", "is_superuser"]}}]	7	024978c2-f9f8-4ec6-8773-5efaf8f13eea
53	2018-08-13 16:17:07.202918+00	ca3be682-4ee3-4f4f-8c11-b9c9f71f63be	Justin Wright	1	[{"added": {}}]	18	bda0b489-b99e-45f6-93e1-27dfc6942da9
54	2018-08-13 16:17:26.994637+00	98ffe758-e7d0-4539-a213-e4781e6218ee	Freckles	1	[{"added": {}}]	11	bda0b489-b99e-45f6-93e1-27dfc6942da9
55	2018-08-13 16:18:11.284302+00	3a7efca6-f5f7-49b8-a420-4e233f658bb1	Justin Wright: Freckles	1	[{"added": {}}]	17	bda0b489-b99e-45f6-93e1-27dfc6942da9
56	2018-08-14 18:49:10.711478+00	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	Namon Bills, CC	1	[{"added": {}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
57	2018-08-14 18:49:22.523323+00	583a434e-fd28-4270-b604-f571130096cb	Medical Doctor	1	[{"added": {}}]	9	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
58	2018-08-14 18:49:26.574761+00	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	Namon Bills, MD	2	[{"changed": {"fields": ["title"]}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
59	2018-08-15 00:23:02.464167+00	13571e24-bfb8-4729-949a-f617bcf2f70a	Bryce Bartel, MD	1	[{"added": {}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
60	2018-08-15 19:46:30.458592+00	13571e24-bfb8-4729-949a-f617bcf2f70a	Bryce Bartel, MD	2	[{"changed": {"fields": ["status"]}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
61	2018-08-15 19:57:24.125824+00	53891105-e227-4398-91ac-3b0349eecb85	Depression	1	[{"added": {}}]	29	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
62	2018-08-15 19:58:02.930503+00	9d66b3c9-e2f2-4140-b666-24961aa3c433	Manage Depression Symptoms	1	[{"added": {}}]	23	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
63	2018-08-15 19:58:43.391472+00	9ceaaf5e-3a98-4547-a0f9-4ed8f2e1ab35	Call Patient	1	[{"added": {}}]	25	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
64	2018-08-15 19:59:04.01076+00	2710636b-cebf-4b6e-84d3-9e6c548446aa	Depression	1	[{"added": {}}]	24	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
65	2018-08-15 20:00:55.167253+00	025d38f5-e586-4e4a-b0c1-5587f470b498	Depression message	1	[{"added": {}}]	28	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
66	2018-08-15 20:01:05.787101+00	664bcbcc-d246-458f-b27d-8a22ca4665f9	Depression message	1	[{"added": {}}]	28	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
67	2018-08-15 20:01:14.432234+00	04cc6f04-5d3f-4c27-87c9-961a0c045d0e	Depression message	1	[{"added": {}}]	28	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
68	2018-08-15 20:01:38.966397+00	1ade354e-8b0c-4ca0-a376-e76c0a8dc67b	Patient Test: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
69	2018-08-15 20:01:44.317819+00	50bc894f-9889-43fc-b4af-1f87c1962630	Daniel Beus: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
70	2018-08-15 20:01:49.371823+00	e0034f82-bee9-4347-905d-d03fd853493d	Evan Sevy: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
71	2018-08-15 20:01:54.779117+00	62cfb8b3-fba2-44ee-aa10-d3219728fa45	Justin Wright: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
72	2018-08-15 20:02:10.329978+00	e7f8581c-f1d9-4257-bc99-3676f67ec8ba	PlanConsent object (e7f8581c-f1d9-4257-bc99-3676f67ec8ba)	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
73	2018-08-15 20:02:17.816994+00	0abfb5b5-2a13-49f8-8d2c-38dc39a68c88	PlanConsent object (0abfb5b5-2a13-49f8-8d2c-38dc39a68c88)	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
74	2018-08-15 20:02:24.811646+00	79a843cc-e3d4-4fab-9729-bf501b6b1393	PlanConsent object (79a843cc-e3d4-4fab-9729-bf501b6b1393)	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
75	2018-08-15 20:02:30.962903+00	b133eb07-5c38-415c-92c6-aebcce16336c	PlanConsent object (b133eb07-5c38-415c-92c6-aebcce16336c)	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
76	2018-08-15 20:05:53.097808+00	b133eb07-5c38-415c-92c6-aebcce16336c	PlanConsent object (b133eb07-5c38-415c-92c6-aebcce16336c)	2	[{"changed": {"fields": ["will_complete_tasks"]}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
77	2018-08-15 20:06:00.971654+00	b133eb07-5c38-415c-92c6-aebcce16336c	PlanConsent object (b133eb07-5c38-415c-92c6-aebcce16336c)	2	[{"changed": {"fields": ["will_complete_tasks"]}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
78	2018-08-30 19:57:26.039834+00	e0034f82-bee9-4347-905d-d03fd853493d	Evan Sevy: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
79	2018-08-30 19:57:26.042357+00	62cfb8b3-fba2-44ee-aa10-d3219728fa45	Justin Wright: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
80	2018-08-30 19:57:26.044074+00	50bc894f-9889-43fc-b4af-1f87c1962630	Daniel Beus: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
81	2018-08-30 19:57:26.045597+00	1ade354e-8b0c-4ca0-a376-e76c0a8dc67b	Patient Test: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
82	2018-08-30 19:57:34.527773+00	2710636b-cebf-4b6e-84d3-9e6c548446aa	Depression	3		24	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
83	2018-08-30 19:57:40.385547+00	9d66b3c9-e2f2-4140-b666-24961aa3c433	Manage Depression Symptoms	3		23	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
84	2018-08-30 19:57:45.508456+00	53891105-e227-4398-91ac-3b0349eecb85	Depression	3		29	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
85	2018-08-30 19:58:01.321919+00	9ceaaf5e-3a98-4547-a0f9-4ed8f2e1ab35	Call Patient	3		25	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
86	2018-08-30 20:23:38.37907+00	d614aed3-8461-4ed2-afa7-df3664725800	Depression	1	[{"added": {}}]	24	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
87	2018-08-30 20:23:39.576413+00	07badb7c-5ab5-434e-94b6-b31ac7e97dbc	Daniel Beus: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
88	2018-08-30 20:23:51.721298+00	0a00e55e-9394-452c-8632-280abd6e3379	CareTeamMember object (0a00e55e-9394-452c-8632-280abd6e3379)	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
89	2018-08-30 20:24:34.262634+00	7d616aeb-dadf-44a8-b47f-b56297d4eaa2	Manage Depression Symptoms	1	[{"added": {}}]	33	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
90	2018-08-30 20:24:47.930056+00	5e359e99-3824-488e-9602-5c11b58c16bf	Depression	1	[{"added": {}}]	36	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
91	2018-08-30 20:24:56.771817+00	d0bdd63e-8102-496d-a317-07cafc22fef9	Depression message	1	[{"added": {}}]	30	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
92	2018-08-30 20:25:11.103029+00	5e359e99-3824-488e-9602-5c11b58c16bf	Depression Education	2	[{"changed": {"fields": ["name"]}}]	36	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
93	2018-08-30 20:25:50.189642+00	1b7c2bf5-0180-4ed4-ae72-fa454b960cf2	Eat Food	1	[{"added": {}}]	34	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
94	2018-08-30 20:26:18.653943+00	6b35be7c-427f-40bd-977e-468746e946f2	Daniel Beus	2	[{"changed": {"fields": ["status"]}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
95	2018-08-30 20:26:22.884735+00	83437bc8-ac13-47f7-a1fd-727fc4d40b8d	Evan Sevy	2	[{"changed": {"fields": ["status"]}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
96	2018-08-30 20:26:34.289578+00	78d5472b-32d4-4b15-8dd1-f14a65070da4	Patient Test	2	[{"changed": {"fields": ["status"]}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
97	2018-08-30 20:26:38.400077+00	ca3be682-4ee3-4f4f-8c11-b9c9f71f63be	Justin Wright	2	[{"changed": {"fields": ["status"]}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
98	2018-08-30 20:27:09.327172+00	0509a951-8c13-4ca6-99c2-99e603d53870	Daniel Beus Depression Plan Concent	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
99	2018-08-30 20:27:46.731997+00	821c347e-4ab2-4b6e-b72d-d3326e8ce0ae	Call Patient	1	[{"added": {}}]	32	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
100	2018-08-30 20:29:52.555288+00	0908fca7-7dca-4acd-8d4b-2be8a9aec423	Evan Sevy: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
101	2018-08-30 20:30:07.982274+00	e78afb29-e874-424e-92e7-6245f8190beb	Medical Doctor	1	[{"added": {}}]	16	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
102	2018-08-30 20:30:14.108616+00	4b36c441-71f8-499b-b0e8-de43c2bdc88d	CareTeamMember object (4b36c441-71f8-499b-b0e8-de43c2bdc88d)	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
103	2018-08-30 20:30:21.927549+00	64072694-089a-4a7e-9ee1-5cb7f29fb399	CareTeamMember object (64072694-089a-4a7e-9ee1-5cb7f29fb399)	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
104	2018-08-30 20:30:30.426871+00	153b0789-821b-41ed-afda-6201605d97ed	CareTeamMember object (153b0789-821b-41ed-afda-6201605d97ed)	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
105	2018-08-30 20:30:52.669186+00	0f99d42d-8ad1-4044-ae5a-f9103799218d	Evan Sevy Depression Plan Concent	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
106	2018-09-05 20:43:32.412946+00	01cbc1e6-4582-4e31-a38b-20a8605e835c	Tyler Delange, MD	1	[{"added": {}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
107	2018-09-06 19:27:11.211587+00	b8450617-013e-4075-8dc1-1c606dac3974	Depression	1	[{"added": {}}]	24	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
108	2018-09-06 19:27:17.582171+00	538c9c4a-f592-440d-8db4-3eab9f0f28ba	Daniel Beus: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
109	2018-09-06 19:27:24.715384+00	12524fb2-3b3c-44b3-9d29-6cd8bb747853	Evan Sevy: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
110	2018-09-06 19:27:34.738252+00	bc621634-7d35-4acf-95d7-796a6c47878e	Jordan Price, Care Manager for Daniel Beus: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
111	2018-09-06 19:27:40.995293+00	4b8f2f90-396c-4ac8-a5a3-f5744b853493	Jordan Price, Care Manager for Evan Sevy: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
112	2018-09-06 19:28:14.096341+00	20169d40-a0b5-4701-93a5-0c591a78225d	Manage Depression Symptoms	1	[{"added": {}}]	33	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
113	2018-09-06 19:28:33.906553+00	90940e09-ee7a-452e-b83b-6a31ae592e2d	Depression Support Messages	1	[{"added": {}}]	36	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
114	2018-09-06 19:28:47.081653+00	6c959320-d66a-487e-858f-a5bba3b14531	Depression Support Messages message	1	[{"added": {}}]	30	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
115	2018-09-06 19:29:21.422407+00	9502ded8-9519-4dbb-9ced-8c78b6c94b31	Daniel Beus Amoxicillin 10mg, daily at 10:00:00	1	[{"added": {}}]	38	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
116	2018-09-06 19:30:40.870076+00	17ebb4d3-5704-49d2-8bea-c226d5ba9897	Call Doctor	1	[{"added": {}}]	34	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
117	2018-09-06 19:31:00.370329+00	538c9c4a-f592-440d-8db4-3eab9f0f28ba	Daniel Beus: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
118	2018-09-06 19:31:04.182453+00	12524fb2-3b3c-44b3-9d29-6cd8bb747853	Evan Sevy: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
119	2018-09-06 19:32:09.613809+00	8c0bbc2c-bf66-47b4-af72-565e75086fa2	Eat Food	1	[{"added": {}}]	34	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
120	2018-09-06 19:32:24.083281+00	19aa5a84-15ce-4942-a4dc-84480312137c	Daniel Beus: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
121	2018-09-06 19:32:28.827003+00	dfa839c1-76a8-4b07-b27e-dba990504c5c	Evan Sevy: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
122	2018-09-06 19:41:01.405655+00	66e58bbf-ff42-4004-9450-6b75d3a97b49	Jordan Price, Care Manager for Daniel Beus: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
123	2018-09-11 09:46:28.887679+00	719563fb-6394-47b8-89e0-3f6f4fad9c9f	Depression	1	[{"added": {}}]	24	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
124	2018-09-11 09:47:00.280057+00	f5b4a640-5edc-4f02-b10b-e39f54df9c4d	Manage Depression Symptoms	1	[{"added": {}}]	33	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
125	2018-09-11 09:47:27.549169+00	8bd270e2-bd11-45db-9167-d4b9c9a07e19	Depression Support	1	[{"added": {}}]	36	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
126	2018-09-11 09:47:31.715861+00	8bd270e2-bd11-45db-9167-d4b9c9a07e19	Depression Support Messages	2	[{"changed": {"fields": ["name"]}}]	36	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
127	2018-09-11 09:47:39.776869+00	3f16806b-85e1-4cbf-a143-5cbf2ad2d0a7	Depression Support Messages message	1	[{"added": {}}]	30	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
128	2018-09-11 09:51:05.918264+00	9a67cb3a-debc-4c7a-ba45-5bb073db776f	Depression Assessment	1	[{"added": {}}, {"added": {"object": "Depression Assessment: Rate your happiness", "name": "assessment question"}}, {"added": {"object": "Depression Assessment: How are you feeling physically?", "name": "assessment question"}}]	40	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
129	2018-09-11 09:51:59.036332+00	ca176f3f-2425-4b38-ab30-bfa62a33f65b	Call Doctor	1	[{"added": {}}]	51	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
130	2018-09-11 09:52:21.8006+00	c93cd17c-e660-4801-a266-609237398341	Eat Food	1	[{"added": {}}]	51	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
131	2018-09-11 09:53:25.007839+00	c93cd17c-e660-4801-a266-609237398341	Eat Breakfast	2	[{"changed": {"fields": ["appear_time", "name"]}}]	51	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
132	2018-09-11 09:54:59.604948+00	58fe54a7-c309-44c2-a385-30dfb26de16e	Eat Lunch	1	[{"added": {}}]	51	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
133	2018-09-11 09:55:07.795688+00	58fe54a7-c309-44c2-a385-30dfb26de16e	Eat Lunch	2	[{"changed": {"fields": ["frequency"]}}]	51	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
134	2018-09-11 09:55:34.82712+00	c93cd17c-e660-4801-a266-609237398341	Eat Breakfast	2	[{"changed": {"fields": ["due_time"]}}]	51	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
135	2018-09-11 09:56:00.886245+00	444eb230-19e1-45da-86db-b5421e3bb1f0	Eat Dinner	1	[{"added": {}}]	51	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
136	2018-09-11 09:56:10.300194+00	58fe54a7-c309-44c2-a385-30dfb26de16e	Eat Lunch	2	[{"changed": {"fields": ["due_time"]}}]	51	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
137	2018-09-11 09:58:18.533693+00	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	Depression symptom report template	1	[{"added": {}}]	42	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
138	2018-09-11 09:58:26.474128+00	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	Depression symptom report template	2	[{"changed": {"fields": ["start_on_day"]}}]	42	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
139	2018-09-11 09:59:04.226606+00	070b5b6b-7ffc-4d42-ace4-bb861a5305ba	Check Reports	1	[{"added": {}}]	50	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
140	2018-09-11 09:59:18.848658+00	070b5b6b-7ffc-4d42-ace4-bb861a5305ba	Check Reports	2	[{"changed": {"fields": ["appear_time"]}}]	50	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
141	2018-09-11 09:59:27.125671+00	070b5b6b-7ffc-4d42-ace4-bb861a5305ba	Check Reports	2	[{"changed": {"fields": ["appear_time"]}}]	50	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
142	2018-09-11 09:59:45.837304+00	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	Depression symptom report template	2	[{"changed": {"fields": ["appear_time"]}}]	42	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
143	2018-09-11 10:00:03.268731+00	42106cc4-60fa-4506-b420-b5a86e86175b	Daniel Beus: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
144	2018-09-11 10:00:08.90318+00	1810d4f1-99ee-485b-aa21-f3c5bb0d88c5	Evan Sevy: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
145	2018-09-11 10:00:16.858083+00	e5a608a6-de00-4a4f-8f65-9889438dd377	Patient Test: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
146	2018-09-11 10:00:24.787332+00	1e11f5ee-21f3-4920-b551-f3938d5c3d4a	Justin Wright: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
147	2018-09-11 10:00:50.273667+00	1225d64d-0494-4ffd-8d91-37cebc7d2408	Jordan Price, Medical Doctor for Daniel Beus: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
148	2018-09-11 10:01:02.612821+00	7d66cb91-f554-4372-ac4d-3ee872336f9c	Namon Bills, Care Manager for Daniel Beus: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
149	2018-09-11 10:01:11.428883+00	b9336698-1373-4edb-8588-2b0b55f3e66a	Bryce Bartel, Care Manager for Evan Sevy: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
150	2018-09-11 10:01:20.880276+00	33759358-45d9-4133-82ea-4cfc4e158cea	Jordan Price, Medical Doctor for Evan Sevy: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
151	2018-09-11 10:01:29.032238+00	42be6794-7a0a-4f60-8904-ac1501c68d6f	Jordan Price, Care Manager for Patient Test: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
152	2018-09-11 10:01:34.861521+00	9dd40f28-a8ac-4e5f-9f34-e7ecf82d28a8	Namon Bills, Medical Doctor for Patient Test: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
153	2018-09-11 10:10:46.378729+00	13df2538-9965-4ca7-85d4-71ed1ab55f18	Daniel Daniel's assessment report due by 2018-09-11 04:10:23-06:00	1	[{"added": {}}, {"added": {"object": "Depression Assessment: Rate your happiness (rated: 3)", "name": "assessment response"}}, {"added": {"object": "Depression Assessment: How are you feeling physically? (rated: 5)", "name": "assessment response"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
154	2018-09-11 10:11:16.363118+00	3d8f2d1c-0787-437f-a53f-af1fd8ca20e2	Evan Evan's assessment report due by 2018-09-11 04:11:09-06:00	1	[{"added": {}}, {"added": {"object": "Depression Assessment: Rate your happiness (rated: 2)", "name": "assessment response"}}, {"added": {"object": "Depression Assessment: How are you feeling physically? (rated: 4)", "name": "assessment response"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
155	2018-09-11 10:11:40.055338+00	7c833800-4570-4e26-ac04-ed0b93c1c125	Patient Patient's assessment report due by 2018-09-11 04:11:28-06:00	1	[{"added": {}}, {"added": {"object": "Depression Assessment: Rate your happiness (rated: 5)", "name": "assessment response"}}, {"added": {"object": "Depression Assessment: How are you feeling physically? (rated: 3)", "name": "assessment response"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
156	2018-09-11 10:12:17.72638+00	a344d800-55b3-4853-83cb-1c814a75a9c2	Fatigue	1	[{"added": {}}]	39	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
157	2018-09-11 10:12:29.039812+00	0c3bf862-ca7c-42d6-9d42-6b7995919973	Pain	1	[{"added": {}}]	39	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
158	2018-09-11 10:12:45.094116+00	59e4c38c-8076-477e-a1c4-bf8de5db6764	Daniel Daniel's symptom report due by 2018-09-11 04:12:04-06:00	1	[{"added": {}}, {"added": {"object": "Daniel Beus Fatigue: 1", "name": "symptom rating"}}, {"added": {"object": "Daniel Beus Pain: 5", "name": "symptom rating"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
159	2018-09-11 10:13:10.729064+00	fbcc51e8-97ec-4dd1-bd2f-f222cce38116	Evan Evan's symptom report due by 2018-09-11 04:13:02-06:00	1	[{"added": {}}, {"added": {"object": "Evan Sevy Fatigue: 3", "name": "symptom rating"}}, {"added": {"object": "Evan Sevy Pain: 2", "name": "symptom rating"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
160	2018-09-11 10:13:35.160607+00	51684a58-d573-4c85-afd2-a2ad1bdba63d	Patient Patient's symptom report due by 2018-09-11 04:13:18-06:00	1	[{"added": {}}, {"added": {"object": "Patient Test Fatigue: 3", "name": "symptom rating"}}, {"added": {"object": "Patient Test Pain: 5", "name": "symptom rating"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
161	2018-09-11 10:14:49.513863+00	d49ed3a2-3625-4bf3-bd91-10e2dec10cc3	Patient Test: Amoxicillin	1	[{"added": {}}]	26	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
162	2018-09-11 10:14:59.618608+00	825f7104-14b7-45a0-8526-efb22548200e	Patient Test Amoxicillin 10mg, daily at 07:00:00	1	[{"added": {}}]	41	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
163	2018-09-11 10:15:12.60335+00	9ee17e2f-6b1a-4b07-9966-a785dbd2810e	Patient Test Amoxicillin 10mg, at 2018-09-11 04:15:02-06:00	1	[{"added": {}}]	46	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
164	2018-09-11 10:15:16.610741+00	9ee17e2f-6b1a-4b07-9966-a785dbd2810e	Patient Test Amoxicillin 10mg, at 2018-09-11 04:15:02-06:00	2	[{"changed": {"fields": ["status"]}}]	46	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
165	2018-09-11 10:15:42.81349+00	2c170038-3c45-4fb1-b628-d475ffd061a1	Daniel Beus Amoxicillin 10mg, daily at 07:00:00	1	[{"added": {}}]	41	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
166	2018-09-11 10:15:46.777729+00	e8d0aa96-bc6a-4c80-9138-876b0713bffb	Daniel Beus Amoxicillin 10mg, at 2018-09-11 04:15:21-06:00	1	[{"added": {}}]	46	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
167	2018-09-11 10:16:24.589818+00	55137693-62f6-48f9-a6e1-14c6239323a1	Evan Sevy: Amoxicillin	1	[{"added": {}}]	26	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
168	2018-09-11 10:16:26.255441+00	8bb87594-0824-4685-88f3-c5daf5fd795e	Evan Sevy Amoxicillin 10mg, daily at 07:00:00	1	[{"added": {}}]	41	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
169	2018-09-11 10:16:29.625883+00	41d955dc-4a0b-4590-b599-28aee7c773fb	Evan Sevy Amoxicillin 10mg, at 2018-09-11 04:16:27-06:00	1	[{"added": {}}]	46	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
170	2018-09-11 10:16:48.509331+00	2c170038-3c45-4fb1-b628-d475ffd061a1	Daniel Beus Amoxicillin 10mg, daily at 07:00:00	2	[{"changed": {"fields": ["repeat_amount"]}}]	41	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
171	2018-09-11 10:16:53.389908+00	e8d0aa96-bc6a-4c80-9138-876b0713bffb	Daniel Beus Amoxicillin 10mg, at 2018-09-11 04:15:21-06:00	2	[]	46	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
172	2018-09-11 20:12:31.708049+00	9ee17e2f-6b1a-4b07-9966-a785dbd2810e	Patient Test Amoxicillin 10mg, at 2018-09-11 06:00:00-06:00	2	[{"changed": {"fields": ["appear_datetime", "due_datetime"]}}]	46	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
173	2018-09-12 03:18:55.807062+00	f56fe653-5b3c-493d-86f5-ec7dbd932dde	Jordan Gunderson, MD	1	[{"added": {}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
174	2018-09-14 00:24:35.767397+00	5794fb47-d466-4686-b467-fb6c0124a712	ronil.rufo@gmail.com	2	[{"changed": {"fields": ["first_name", "last_name", "validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
175	2018-09-14 00:25:19.57449+00	ebf7cce4-712f-4583-a398-e77c7686115b	Ronil Rufo	1	[{"added": {}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
176	2018-09-14 23:31:03.073921+00	4d58f161-27f3-4fbe-91b5-930c6b4e2952	jlewis.code@gmail.com	2	[{"changed": {"fields": ["first_name", "last_name", "validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
177	2018-09-14 23:31:50.681136+00	4ab571d9-1ff4-4c34-b21b-3021bd57cf66	Joe Lewis, MD	1	[{"added": {}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
178	2018-09-15 05:01:31.884427+00	deb62432-8faa-4f80-b78e-e48faf6ec4c7	kcole@startstudio.com	2	[{"changed": {"fields": ["first_name", "last_name", "validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
179	2018-09-15 05:01:53.196819+00	a1d9eeac-8a9d-473d-8eed-f507721aa7c4	Kacey Cole, CC	1	[{"added": {}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
180	2018-09-21 08:29:44.089496+00	ca7fea78-5e6a-49f4-ad78-953e66c7dcbb	Daniel Beus: Test Plan Depression	1	[{"added": {}}]	21	4d58f161-27f3-4fbe-91b5-930c6b4e2952
181	2018-09-25 02:55:01.023148+00	6998f5f2-4396-4f95-9281-1365144c80ef	pat.keeps.looking.up@gmail.com	2	[{"changed": {"fields": ["first_name", "last_name", "validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
182	2018-09-25 02:58:11.588523+00	de594b37-6201-4469-9a33-81fd03e5ad65	Pat Tan, CC	1	[{"added": {}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
183	2018-09-25 19:50:56.225811+00	e5a608a6-de00-4a4f-8f65-9889438dd377	Patient Test: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
184	2018-09-25 19:50:56.228398+00	ca7fea78-5e6a-49f4-ad78-953e66c7dcbb	Daniel Beus: Test Plan Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
185	2018-09-25 19:50:56.230022+00	42106cc4-60fa-4506-b420-b5a86e86175b	Daniel Beus: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
186	2018-09-25 19:50:56.231696+00	1e11f5ee-21f3-4920-b551-f3938d5c3d4a	Justin Wright: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
187	2018-09-25 19:50:56.233398+00	1810d4f1-99ee-485b-aa21-f3c5bb0d88c5	Evan Sevy: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
188	2018-09-25 19:54:51.095974+00	6b6df74f-1f39-44ef-8555-81f0a9aa8923	Take Blood Pressure	2	[{"added": {"name": "vital question", "object": "Take Blood Pressure: What time did you go to bed?"}}, {"added": {"name": "vital question", "object": "Take Blood Pressure: What time did you get up?"}}, {"added": {"name": "vital question", "object": "Take Blood Pressure: How did you feel when you got up?"}}, {"added": {"name": "vital question", "object": "Take Blood Pressure: Rate the quality of your sleep"}}]	55	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
189	2018-09-25 19:55:30.807881+00	6b6df74f-1f39-44ef-8555-81f0a9aa8923	Sleep Report	2	[{"changed": {"fields": ["name"]}}]	55	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
190	2018-09-25 19:56:48.993457+00	b9c80f83-7aa9-47ff-aeb4-4dbec38daa92	Patient Test: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
191	2018-09-25 19:57:36.37238+00	3159b486-64e1-4188-9949-bc676725ad48	Patient Test Amoxicillin 10mg, every_other_day at 09:00:00	1	[{"added": {}}]	41	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
192	2018-09-25 19:58:56.783661+00	e5e27c9c-9a06-4925-b592-bdb1bf889d3c	Patient Test: Depression: Manage Depression Symptoms	1	[{"added": {}}]	23	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
193	2018-09-25 20:01:11.064593+00	ffec83fe-aded-4f38-bb8a-83bee8ef4638	Jordan Price, Medical Doctor for Patient Test: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
194	2018-09-25 20:01:28.924712+00	5a895cb6-e0c7-4cd7-8a06-b8de5a035325	Namon Bills, Care Manager for Patient Test: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
195	2018-09-25 20:11:20.903327+00	aa7b5096-cb8d-4f37-9971-5f94d1495f07	Patient Test Depression Plan Consent	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
196	2018-09-25 20:19:40.592807+00	ca4de767-20fc-4ada-89a8-4804b26e8f55	Patient Patient's assessment report due by 2018-09-25 17:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 4)"}}, {"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 3)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
197	2018-09-25 20:30:10.26012+00	cf9f0f4e-79e0-4a3d-91e8-b5d05cd0d04c	PatientTask object (cf9f0f4e-79e0-4a3d-91e8-b5d05cd0d04c)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
198	2018-09-25 20:33:14.807285+00	6b6df74f-1f39-44ef-8555-81f0a9aa8923	Sleep Report	2	[{"changed": {"fields": ["frequency"]}}]	55	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
199	2018-09-25 20:33:51.519239+00	b9c80f83-7aa9-47ff-aeb4-4dbec38daa92	Patient Test: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
200	2018-09-25 20:44:15.926624+00	6b6df74f-1f39-44ef-8555-81f0a9aa8923	Sleep Report	2	[{"changed": {"fields": ["start_on_day"]}}]	55	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
201	2018-09-26 03:08:12.128242+00	9c8049a2-86ef-4477-a223-2ef29b39d0ac	Patient Test: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
202	2018-09-26 19:35:19.278336+00	df047e01-541f-41cc-8da6-036edae237da	Patient Test: Terrible Problem Area	1	[{"added": {}}]	19	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
203	2018-09-26 19:35:55.556015+00	fcb346e0-b299-45ad-a549-f44080568210	Jordan Price, Care Manager for Patient Test: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
204	2018-09-26 19:43:30.653304+00	f2f38406-700d-4ed5-9f1b-3ffef814a980	Patient Test Depression Plan Consent	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
205	2018-09-26 19:47:04.434121+00	09323849-ac75-4653-950e-cbe0f2ac4ecb	Patient Test: Depression: Manage Depression Symptoms	1	[{"added": {}}]	23	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
206	2018-09-26 19:47:12.133669+00	03ffe227-1277-475d-a93e-cb9ac3e79395	Manage Depression Symptoms: 5	1	[{"added": {}}]	53	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
207	2018-09-26 19:48:19.717331+00	20978199-5d4c-4693-9d49-3e0cc9d51dd6	Patient Test: Depression: Manage Depression Symptoms - patient@test.com: adsfasdf	1	[{"added": {}}]	54	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
208	2018-09-26 21:06:14.825806+00	cb27a235-4a84-4af0-8ef5-cf6b13b7dfda	TeamTask object (cb27a235-4a84-4af0-8ef5-cf6b13b7dfda)	1	[{"added": {}}]	45	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
209	2018-10-02 19:55:21.961501+00	e0d977d0-3859-4f39-9c05-135cadcdc6f4	Daniel Beus: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
210	2018-10-02 20:01:00.293637+00	53ae9f40-29de-424f-ada7-f2750c519b88	Daniel Daniel's assessment report due by 2018-10-02 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 5)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
211	2018-10-02 20:01:12.923614+00	53ae9f40-29de-424f-ada7-f2750c519b88	Daniel Daniel's assessment report due by 2018-10-02 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 5)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
212	2018-10-02 20:08:22.991976+00	2b54437b-bbfe-4acf-a7e0-e60212c7f74a	Patient Patient's assessment report due by 2018-09-26 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 3)"}}, {"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 4)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
213	2018-10-02 20:08:32.813354+00	3276421c-321f-4a83-8dc0-82f741becc78	Patient Patient's assessment report due by 2018-09-27 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 5)"}}, {"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 3)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
214	2018-10-02 20:08:40.864122+00	1866dea1-955b-496b-9887-1441734f2f89	Patient Patient's assessment report due by 2018-09-28 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 3)"}}, {"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 2)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
215	2018-10-02 20:08:50.283341+00	4a5ce7e2-4240-48e5-bd31-4da963aabfe6	Patient Patient's assessment report due by 2018-09-29 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 3)"}}, {"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 4)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
216	2018-10-05 20:16:54.154006+00	e0d977d0-3859-4f39-9c05-135cadcdc6f4	Daniel Beus: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
217	2018-10-05 20:16:54.156754+00	9c8049a2-86ef-4477-a223-2ef29b39d0ac	Patient Test: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
218	2018-10-05 20:16:54.158338+00	74687436-afcd-4c50-9670-28734c692025	Daniel Beus: Test Plan Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
219	2018-10-05 20:21:38.899647+00	fdb25787-150f-4117-a757-b1cd399b98f3	Daniel Beus: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
220	2018-10-05 20:21:44.560427+00	0a5f31e6-9573-4acd-b701-5a4ba347dd37	Patient Test: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
221	2018-10-05 20:21:59.142199+00	141ed317-4a19-4a30-b245-4909bf6a9767	Daniel Beus: Test Plan Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
222	2018-10-08 08:47:33.269506+00	32e68c59-e41a-4bfa-8bc8-deeb261182cd	jprice@izeni.com	1	[{"added": {}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
223	2018-10-08 08:47:42.644051+00	32e68c59-e41a-4bfa-8bc8-deeb261182cd	jprice@izeni.com	2	[{"changed": {"fields": ["validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
224	2018-10-08 20:27:10.723786+00	8c4d0eb9-c9fd-463a-831e-ab1220b06a93	Patient Test Amoxicillin 10mg, daily at 09:00:00	1	[{"added": {}}]	41	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
225	2018-10-08 20:27:32.392545+00	52bd6b93-bc7a-4b71-a092-8beeb85bb2f3	Patient Test Amoxicillin 10mg, at 2018-10-08 09:00:00-06:00	1	[{"added": {}}]	46	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
226	2018-10-08 20:29:59.466553+00	68523cec-50cb-4510-9508-99983fb0c8de	Jordan Price, CC	2	[{"changed": {"fields": ["facilities"]}}]	10	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
227	2018-10-10 21:56:36.569682+00	e636f748-9511-4537-9014-64e93b7dca78	Daniel Beus Amoxicillin 10mg, once at 09:00:00	1	[{"added": {}}]	41	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
263	2018-10-16 23:30:29.641936+00	c6230196-44bd-4284-9b7a-a2d28e6686ff	Jordan Price Amoxicillin 10mg, at 2018-10-16 03:00:00-06:00	2	[{"changed": {"fields": ["status"]}}]	46	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
264	2018-10-16 23:30:56.012295+00	c6230196-44bd-4284-9b7a-a2d28e6686ff	Jordan Price Amoxicillin 10mg, at 2018-10-16 03:00:00-06:00	2	[{"changed": {"fields": ["status"]}}]	46	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
265	2018-10-16 23:31:07.116064+00	c6230196-44bd-4284-9b7a-a2d28e6686ff	Jordan Price Amoxicillin 10mg, at 2018-10-16 03:00:00-06:00	2	[{"changed": {"fields": ["status"]}}]	46	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
228	2018-10-10 22:14:02.735092+00	81763a50-ffd2-4da0-a357-59d9f070953e	Patient Test's vital report due by 2018-10-05 09:03:00-06:00	2	[{"added": {"name": "vital response", "object": "Sleep Report:What is the difference between -1 and 1? (answer: 1.0)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What was the weather like last night? (answer: rainy)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How many trips to the bathroom? (answer: 1)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How was your energy? (answer: 3)"}}, {"added": {"name": "vital response", "object": "Sleep Report:Rate the quality of your sleep (answer: 5)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What time did you go to bed? (answer: 16:12:48)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What time did you get up? (answer: 16:12:53)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How did you feel when you got up? (answer: 3)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How many trips to the bathroom? (answer: None)"}}]	56	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
229	2018-10-10 22:28:04.624301+00	0dcda8f1-2e69-4842-8fe2-a2231c56e79d	Patient Test's vital report due by 2018-10-10 09:03:00-06:00	2	[{"added": {"name": "vital response", "object": "Sleep Report:What time did you go to bed? (answer: 16:26:54)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What time did you get up? (answer: 16:26:57)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How did you feel when you got up? (answer: 3)"}}, {"added": {"name": "vital response", "object": "Sleep Report:Rate the quality of your sleep (answer: 4)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How was your energy? (answer: 5)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How many trips to the bathroom? (answer: 0)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How many trips to the bathroom? (answer: 1)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What was the weather like last night? (answer: rainy)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What is the difference between -1 and 1? (answer: 1.1)"}}]	56	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
230	2018-10-16 21:12:50.602784+00	6221a021-e750-4ec5-b2f2-f6e42c6969e0	Justin Wright	3		14	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
231	2018-10-16 21:13:39.089973+00	d140a271-3f1f-494e-8e2e-e86bdf84e743	Jordan Price, Care Manager for Daniel Beus: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
232	2018-10-16 21:13:48.629379+00	4ba0968c-06bc-446c-90e6-f3166927c7ad	Namon Bills, Medical Doctor for Daniel Beus: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
233	2018-10-16 21:13:55.645685+00	8a011773-2760-4899-b108-7b5b9e31634e	Jordan Price, Care Manager for Patient Test: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
234	2018-10-16 21:14:02.482898+00	79a8fadf-908f-4e7b-8b60-ffaa4388e67e	Namon Bills, Medical Doctor for Patient Test: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
235	2018-10-16 21:15:03.75046+00	0a5f31e6-9573-4acd-b701-5a4ba347dd37	Patient Test: Depression	3		21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
236	2018-10-16 21:15:58.819096+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	Patient Test: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
237	2018-10-16 21:16:33.51266+00	cffbe6b3-3c7a-44a0-93b2-7abdfed5fdf8	Patient Test Depression Plan Consent	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
238	2018-10-16 21:16:40.89136+00	f3deb40c-5f67-4c70-acd6-2278b441e0fa	Daniel Beus Depression Plan Consent	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
239	2018-10-16 21:16:50.752692+00	abacd08a-4147-408b-b925-0a8339703488	Jordan Price, Care Manager for Patient Test: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
240	2018-10-16 21:16:57.382059+00	bc9fd625-da47-4a21-aece-0754d9b87865	Namon Bills, Medical Doctor for Patient Test: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
241	2018-10-16 21:26:33.896417+00	7360410a-a370-4a02-afe3-f7a755315cea	Manage Depression Symptoms: 2	1	[{"added": {}}]	53	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
242	2018-10-16 21:29:44.799894+00	a74ec5fd-51e8-40d8-92fe-c400fe206496	Patient Test: Depression: Manage Depression Symptoms - jprice@startstudio.com: I'm commenting on your goal	1	[{"added": {}}]	54	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
243	2018-10-16 21:29:59.136201+00	cf4d71f8-4b61-4522-a606-6b98db9c7c99	Daniel Beus: Depression: Manage Depression Symptoms - dbeus@mindfiretechnology.com: I'm commenting on my goal	1	[{"added": {}}]	54	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
244	2018-10-16 21:33:27.289588+00	a74ec5fd-51e8-40d8-92fe-c400fe206496	Daniel Beus: Depression: Manage Depression Symptoms - jprice@startstudio.com: I'm commenting on your goal	2	[{"changed": {"fields": ["goal"]}}]	54	024978c2-f9f8-4ec6-8773-5efaf8f13eea
245	2018-10-16 21:44:00.498808+00	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb	Daniel Beus Amoxicillin 10mg, daily at 09:00:00	1	[{"added": {}}]	41	024978c2-f9f8-4ec6-8773-5efaf8f13eea
246	2018-10-16 23:11:29.140042+00	77fff1ef-c055-4e53-9af5-3492b45b5e14	Justin Wright: Justin Wright	3		19	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
247	2018-10-16 23:12:06.656085+00	32e68c59-e41a-4bfa-8bc8-deeb261182cd	jprice@izeni.com	3		7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
248	2018-10-16 23:12:23.447161+00	39c8deae-045f-4d48-a68e-fd375be04c3e	jprice@izeni.com	1	[{"added": {}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
249	2018-10-16 23:13:06.196337+00	39c8deae-045f-4d48-a68e-fd375be04c3e	jprice@izeni.com	2	[{"changed": {"fields": ["first_name", "last_name", "validation_key", "validated_at"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
250	2018-10-16 23:13:44.78633+00	182a449d-5871-41fa-ae99-24d61aba25e7	Jordan Price	1	[{"added": {}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
251	2018-10-16 23:14:36.878812+00	7d68bd52-88ba-4706-9704-cb196c7d48cb	Jordan Price: Freckles	1	[{"added": {}}]	17	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
252	2018-10-16 23:14:41.787857+00	182a449d-5871-41fa-ae99-24d61aba25e7	Jordan Price	2	[{"changed": {"fields": ["diagnosis"]}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
253	2018-10-16 23:23:46.614077+00	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8	jprice@startstudio.com	2	[{"changed": {"fields": ["preferred_name"]}}]	7	e5169647-5801-40ff-aa23-147ea5c58c60
254	2018-10-16 23:27:37.30019+00	65dc1c81-7ab3-45fd-8f38-d16bf3e550e6	Jordan Price: Amoxicillin	1	[{"added": {}}]	26	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
255	2018-10-16 23:27:47.978166+00	2418946b-6a8a-447b-b6c0-8779f1927534	Jordan Price: Apendectimy	1	[{"added": {}}]	20	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
256	2018-10-16 23:28:27.070529+00	c48f91ad-8c91-478b-870d-30e5963b515f	Jordan Price: Bad Depression	1	[{"added": {}}]	19	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
257	2018-10-16 23:28:41.964136+00	dd04dc61-5fb0-46cf-a20e-547258f1b9ae	Jordan Price: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
258	2018-10-16 23:28:52.675464+00	45016259-9797-41e5-9589-eba857ababdf	Manage Depression Symptoms: 1	1	[{"added": {}}]	53	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
259	2018-10-16 23:29:08.552948+00	bc55037b-2749-408a-b54e-60b2d9b07b0a	Jordan Price: Depression: Manage Depression Symptoms - jprice@startstudio.com: Comment on goal	1	[{"added": {}}]	54	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
260	2018-10-16 23:29:21.685833+00	5d42dba3-04f3-4954-96e9-cd4a75996896	Jordan Price Depression Plan Consent	1	[{"added": {}}]	22	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
261	2018-10-16 23:29:53.709294+00	33ea685f-4380-4353-8027-ebeae6fdce9b	Jordan Jordan's assessment report due by 2018-10-16 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 3)"}}, {"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 3)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
262	2018-10-16 23:30:21.823063+00	8540e2e9-b1cc-4d2c-a8ae-298cb25d267c	Jordan Price Amoxicillin 10mg, daily at 09:00:00	1	[{"added": {}}]	41	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
266	2018-10-16 23:31:50.961964+00	9aaca106-4c91-4ef7-bf82-46cbb42c38d0	PatientTask object (9aaca106-4c91-4ef7-bf82-46cbb42c38d0)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
267	2018-10-16 23:32:03.552329+00	5ccba1ff-2050-4f45-a7a4-2ee89fe55515	PatientTask object (5ccba1ff-2050-4f45-a7a4-2ee89fe55515)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
268	2018-10-16 23:32:15.013253+00	5573707a-2901-4b06-aa87-e8658578a4f3	PatientTask object (5573707a-2901-4b06-aa87-e8658578a4f3)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
269	2018-10-16 23:32:29.096758+00	6d4c4fe2-fa99-4f70-afb1-7da0c4410594	PatientTask object (6d4c4fe2-fa99-4f70-afb1-7da0c4410594)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
270	2018-10-16 23:33:01.004515+00	556ba139-dcc6-4e0f-8362-080fb7fb0900	Jordan Jordan's symptom report due by 2018-10-17 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Jordan Price Fatigue: 1"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
271	2018-10-16 23:34:19.18677+00	13192281-f947-4c16-87a2-8f126267dbd3	Jordan Price's vital report due by 2018-10-16 09:03:00-06:00	2	[{"added": {"name": "vital response", "object": "Sleep Report:What time did you go to bed? (answer: 17:33:52)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What time did you get up? (answer: 17:33:54)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How did you feel when you got up? (answer: 3)"}}, {"added": {"name": "vital response", "object": "Sleep Report:Rate the quality of your sleep (answer: 3)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How was your energy? (answer: 3)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How many trips to the bathroom? (answer: 1)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How many trips to the bathroom? (answer: 1)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What was the weather like last night? (answer: Stormy)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What is the difference between -1 and 1? (answer: None)"}}]	56	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
272	2018-10-16 23:34:43.038275+00	df9bdd6e-0510-4e1d-965e-c9b13885023e	Jordan Price, Care Manager for Jordan Price: Depression	1	[{"added": {}}]	35	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
273	2018-10-17 01:18:34.420941+00	39c8deae-045f-4d48-a68e-fd375be04c3e	jprice@izeni.com	3		7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
274	2018-10-17 01:18:45.825978+00	36d6501a-d24c-460b-b106-1a2831a575f9	jprice@izeni.com	1	[{"added": {}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
275	2018-10-17 01:22:30.82546+00	7afe399f-1729-4aa8-9ea5-9d5f3b47e818	 	1	[{"added": {}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
276	2018-10-17 01:34:42.685558+00	7afe399f-1729-4aa8-9ea5-9d5f3b47e818	 	2	[{"changed": {"fields": ["status"]}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
277	2018-10-17 01:34:53.631589+00	7afe399f-1729-4aa8-9ea5-9d5f3b47e818	 	3		18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
278	2018-10-17 01:35:13.16686+00	15ce9664-65ca-45c1-8773-9576f45ba928	 	1	[{"added": {}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
279	2018-10-17 06:37:17.587113+00	36d6501a-d24c-460b-b106-1a2831a575f9	jprice@izeni.com	3		7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
280	2018-10-17 06:37:26.981667+00	86b92518-9c2a-4ca8-a471-2860473c4b9e	jprice@izeni.com	1	[{"added": {}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
281	2018-10-17 06:39:46.668198+00	b310af7d-67df-4e4c-a34e-154b25b057ea	 	1	[{"added": {}}]	18	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
282	2018-10-17 06:41:58.1254+00	86b92518-9c2a-4ca8-a471-2860473c4b9e	jprice@izeni.com	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	7	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
283	2018-10-17 07:04:53.59698+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	Jordan Price: Depression	1	[{"added": {}}]	21	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
284	2018-10-17 07:05:09.875435+00	c1531990-8062-468d-9b10-575a0004547c	Manage Depression Symptoms: 1	1	[{"added": {}}]	53	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
285	2018-10-17 07:05:22.372098+00	570e5a30-f150-453e-8397-8ba6b17208c6	Jordan Price: Depression: Manage Depression Symptoms - jprice@izeni.com: Test	1	[{"added": {}}]	54	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
286	2018-10-17 07:05:30.7081+00	3086bc89-41ff-4d31-8b81-399ab5a7c49a	Jordan Price: Depression: Manage Depression Symptoms - jprice@startstudio.com: Test	1	[{"added": {}}]	54	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
287	2018-10-17 07:05:59.677129+00	c1531990-8062-468d-9b10-575a0004547c	Manage Depression Symptoms: 1	2	[{"changed": {"fields": ["goal"]}}]	53	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
288	2018-10-17 19:27:53.946686+00	c72d3ad9-e3a5-4d42-adf2-1a8a229b4546	Jordan Price: Amoxicillin	1	[{"added": {}}]	26	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
289	2018-10-17 19:28:12.527796+00	b4ecef1d-8fd6-4e17-b64a-6a329cf15256	Jordan Price Amoxicillin 10mg, daily at 09:00:00	1	[{"added": {}}]	41	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
290	2018-10-17 20:09:05.236437+00	1	https://careadopt.izeni.net	2	[{"changed": {"fields": ["domain", "name"]}}]	59	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
291	2018-10-17 20:09:24.71705+00	1	careadopt.izeni.net	2	[{"changed": {"fields": ["domain"]}}]	59	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
292	2018-10-24 19:44:29.771143+00	f09e230e-6bbe-49af-8a7b-f0917d122262	PatientTask object (f09e230e-6bbe-49af-8a7b-f0917d122262)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
293	2018-10-24 19:45:33.680063+00	6a4c7537-32a7-4591-a8ee-87c2b66043d7	PatientTask object (6a4c7537-32a7-4591-a8ee-87c2b66043d7)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
294	2018-10-24 19:45:41.783959+00	d6088b84-69da-44aa-a2c4-8d23ba7cb62b	PatientTask object (d6088b84-69da-44aa-a2c4-8d23ba7cb62b)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
295	2018-10-24 19:45:47.309166+00	02713cf0-67aa-4076-840e-57f824b9bca4	PatientTask object (02713cf0-67aa-4076-840e-57f824b9bca4)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
296	2018-10-24 19:45:52.240005+00	c3c814bb-c992-4d8f-8fff-0a015e8d5a63	PatientTask object (c3c814bb-c992-4d8f-8fff-0a015e8d5a63)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
297	2018-10-24 19:45:58.061894+00	0d3e738b-bd42-4581-8516-16532c8142ca	PatientTask object (0d3e738b-bd42-4581-8516-16532c8142ca)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
298	2018-10-24 19:46:02.471124+00	c5e85c44-557a-4d48-b095-60cf73d7e72b	PatientTask object (c5e85c44-557a-4d48-b095-60cf73d7e72b)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
299	2018-10-24 19:46:05.898776+00	56aa5b41-a571-4cb1-bc5e-0ccf98b1ed3b	PatientTask object (56aa5b41-a571-4cb1-bc5e-0ccf98b1ed3b)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
300	2018-10-24 19:46:09.167397+00	31ea2e5c-12a9-4750-95e6-97c5d3960a08	PatientTask object (31ea2e5c-12a9-4750-95e6-97c5d3960a08)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
301	2018-10-24 19:46:29.404785+00	b59cda4f-82a3-40f0-b89b-ca6710b39088	PatientTask object (b59cda4f-82a3-40f0-b89b-ca6710b39088)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
302	2018-10-24 19:46:35.835669+00	485d023a-d51f-40f2-9975-af3abc06f1a4	PatientTask object (485d023a-d51f-40f2-9975-af3abc06f1a4)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
303	2018-10-24 19:46:43.461493+00	0529e786-d9b4-4917-9fc5-996e41bb24e1	PatientTask object (0529e786-d9b4-4917-9fc5-996e41bb24e1)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
304	2018-10-24 19:46:49.59966+00	0478bc32-17ad-4ed3-8dba-6c16a9a74005	PatientTask object (0478bc32-17ad-4ed3-8dba-6c16a9a74005)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
329	2018-10-24 20:03:47.068182+00	b4ceb27d-5ca9-4fc8-97b4-79d9b754effc	Patient Patient's symptom report due by 2018-10-25 17:59:59-06:00	2	[{"deleted": {"name": "symptom rating", "object": "Patient Test Fatigue: 1"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
305	2018-10-24 19:47:18.283885+00	6fae57df-e845-4ca8-b179-3304ce393675	Patient Patient's assessment report due by 2018-10-16 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 5)"}}, {"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 4)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
306	2018-10-24 19:47:33.403666+00	c894932a-818e-4232-800b-0867e3a839d8	Patient Patient's assessment report due by 2018-10-17 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 4)"}}, {"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 4)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
307	2018-10-24 19:47:41.218725+00	8e6c7ee1-5668-4fd3-a8cc-7dfe7d141d35	Patient Patient's assessment report due by 2018-10-18 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 3)"}}, {"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 4)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
308	2018-10-24 19:48:24.683135+00	d0ef3d9e-bf4b-47dc-b9e7-d9859ab9f710	PatientTask object (d0ef3d9e-bf4b-47dc-b9e7-d9859ab9f710)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
309	2018-10-24 19:48:33.207675+00	872c2ee2-6009-4908-8cb9-afa6c4a65dbe	PatientTask object (872c2ee2-6009-4908-8cb9-afa6c4a65dbe)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
310	2018-10-24 19:48:44.910674+00	4a8dd415-a27a-410c-8f19-e18d03466e6a	PatientTask object (4a8dd415-a27a-410c-8f19-e18d03466e6a)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
311	2018-10-24 19:49:26.406929+00	6d3db8cc-2fcd-4326-8f4a-43db1a24efef	PatientTask object (6d3db8cc-2fcd-4326-8f4a-43db1a24efef)	2	[{"changed": {"fields": ["status"]}}]	47	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
312	2018-10-24 19:50:00.775905+00	ae4c5e59-e4db-468f-adcc-5db7e6d7f8bd	Patient Patient's symptom report due by 2018-10-24 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 4"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
313	2018-10-24 19:50:07.140972+00	b4ceb27d-5ca9-4fc8-97b4-79d9b754effc	Patient Patient's symptom report due by 2018-10-25 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Pain: 3"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
314	2018-10-24 19:50:31.813768+00	ca66ea13-74d5-486a-8a33-985dc98dd0c3	Patient Patient's assessment report due by 2018-10-24 11:00:00-06:00	2	[{"added": {"name": "assessment response", "object": "Depression Assessment: Rate your happiness (rated: 4)"}}, {"added": {"name": "assessment response", "object": "Depression Assessment: How are you feeling physically? (rated: 5)"}}]	43	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
315	2018-10-24 19:52:37.032257+00	b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb	Patient Test's vital report due by 2018-10-24 09:03:00-06:00	2	[{"added": {"name": "vital response", "object": "Sleep Report:What time did you go to bed? (answer: 13:52:11)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What time did you get up? (answer: 13:52:12)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How did you feel when you got up? (answer: None)"}}, {"added": {"name": "vital response", "object": "Sleep Report:Rate the quality of your sleep (answer: 5)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How was your energy? (answer: 5)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How many trips to the bathroom? (answer: 1)"}}, {"added": {"name": "vital response", "object": "Sleep Report:How many trips to the bathroom? (answer: 1)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What was the weather like last night? (answer: Good)"}}, {"added": {"name": "vital response", "object": "Sleep Report:What is the difference between -1 and 1? (answer: 1.0)"}}]	56	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
316	2018-10-24 20:00:19.999863+00	904923d9-3e22-4e79-8565-d168680ea660	Patient Patient's symptom report due by 2018-10-17 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 5"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
317	2018-10-24 20:00:35.230166+00	900a4db6-885c-4694-a1af-a94d06482acc	Patient Patient's symptom report due by 2018-10-18 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 4"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
318	2018-10-24 20:01:18.772256+00	904923d9-3e22-4e79-8565-d168680ea660	Patient Patient's symptom report due by 2018-10-17 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Pain: 5"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
319	2018-10-24 20:01:25.343502+00	900a4db6-885c-4694-a1af-a94d06482acc	Patient Patient's symptom report due by 2018-10-18 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Pain: 4"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
320	2018-10-24 20:01:32.009246+00	c6fbda29-dcb4-430c-b5e7-69e455ecd378	Patient Patient's symptom report due by 2018-10-19 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 3"}}, {"added": {"name": "symptom rating", "object": "Patient Test Pain: 3"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
321	2018-10-24 20:01:40.477476+00	ad072c55-516d-4972-ac51-8f7fca2ac486	Patient Patient's symptom report due by 2018-10-20 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 2"}}, {"added": {"name": "symptom rating", "object": "Patient Test Pain: 2"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
322	2018-10-24 20:01:47.576173+00	81ba7a15-7a3d-4ff9-9d03-01bf87a3cf1a	Patient Patient's symptom report due by 2018-10-21 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 1"}}, {"added": {"name": "symptom rating", "object": "Patient Test Pain: 1"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
323	2018-10-24 20:02:03.581929+00	8109432b-9d74-4632-abfe-42fb0c7fa454	Patient Patient's symptom report due by 2018-10-22 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 2"}}, {"added": {"name": "symptom rating", "object": "Patient Test Pain: 2"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
324	2018-10-24 20:02:13.63195+00	354037dc-b621-4597-b861-99b6dadddd9e	Patient Patient's symptom report due by 2018-10-23 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 3"}}, {"added": {"name": "symptom rating", "object": "Patient Test Pain: 3"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
325	2018-10-24 20:02:38.742216+00	ae4c5e59-e4db-468f-adcc-5db7e6d7f8bd	Patient Patient's symptom report due by 2018-10-24 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Pain: 2"}}, {"deleted": {"name": "symptom rating", "object": "Patient Test Fatigue: 4"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
326	2018-10-24 20:02:46.689289+00	ae4c5e59-e4db-468f-adcc-5db7e6d7f8bd	Patient Patient's symptom report due by 2018-10-24 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 2"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
327	2018-10-24 20:02:57.632426+00	b4ceb27d-5ca9-4fc8-97b4-79d9b754effc	Patient Patient's symptom report due by 2018-10-25 17:59:59-06:00	2	[{"deleted": {"name": "symptom rating", "object": "Patient Test Pain: 3"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
328	2018-10-24 20:03:29.057878+00	b4ceb27d-5ca9-4fc8-97b4-79d9b754effc	Patient Patient's symptom report due by 2018-10-25 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 1"}}, {"added": {"name": "symptom rating", "object": "Patient Test Pain: 3"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
330	2018-10-24 20:04:03.50736+00	b4ceb27d-5ca9-4fc8-97b4-79d9b754effc	Patient Patient's symptom report due by 2018-10-25 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Pain: 2"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
331	2018-10-24 20:04:17.367348+00	b4ceb27d-5ca9-4fc8-97b4-79d9b754effc	Patient Patient's symptom report due by 2018-10-25 17:59:59-06:00	2	[{"deleted": {"name": "symptom rating", "object": "Patient Test Pain: 3"}}, {"deleted": {"name": "symptom rating", "object": "Patient Test Pain: 2"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
332	2018-10-24 20:04:54.605757+00	ae4c5e59-e4db-468f-adcc-5db7e6d7f8bd	Patient Patient's symptom report due by 2018-10-24 17:59:59-06:00	2	[{"deleted": {"name": "symptom rating", "object": "Patient Test Pain: 2"}}, {"deleted": {"name": "symptom rating", "object": "Patient Test Fatigue: 2"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
333	2018-10-24 20:05:00.449832+00	354037dc-b621-4597-b861-99b6dadddd9e	Patient Patient's symptom report due by 2018-10-23 17:59:59-06:00	2	[{"deleted": {"name": "symptom rating", "object": "Patient Test Pain: 3"}}, {"deleted": {"name": "symptom rating", "object": "Patient Test Fatigue: 3"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
334	2018-10-24 20:05:30.764684+00	354037dc-b621-4597-b861-99b6dadddd9e	Patient Patient's symptom report due by 2018-10-23 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 2"}}, {"added": {"name": "symptom rating", "object": "Patient Test Pain: 3"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
335	2018-10-24 20:06:01.47929+00	ae4c5e59-e4db-468f-adcc-5db7e6d7f8bd	Patient Patient's symptom report due by 2018-10-24 17:59:59-06:00	2	[{"added": {"name": "symptom rating", "object": "Patient Test Fatigue: 1"}}, {"added": {"name": "symptom rating", "object": "Patient Test Pain: 3"}}]	52	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
336	2018-10-25 18:03:42.772314+00	4b986fdb-14d3-4615-93fa-fa153f69a96c	Jordan Price	1	[{"added": {}}]	65	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 336, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	authtoken	token
7	accounts	emailuser
8	core	providerspecialty
9	core	providertitle
10	core	employeeprofile
11	core	diagnosis
12	core	organization
13	core	procedure
14	core	medication
15	core	facility
16	core	providerrole
17	patients	patientdiagnosis
18	patients	patientprofile
19	patients	problemarea
20	patients	patientprocedure
22	plans	planconsent
23	plans	goal
24	plans	careplantemplate
25	plans	teamtask
26	patients	patientmedication
27	plans	patienttask
28	plans	streammessage
29	plans	messagestream
30	plans	infomessage
31	plans	patienttaskinstance
32	plans	teamtasktemplate
33	plans	goaltemplate
34	plans	patienttasktemplate
35	plans	careteammember
36	plans	infomessagequeue
37	plans	medicationtaskinstance
38	plans	medicationtasktemplate
39	core	symptom
40	tasks	assessmenttasktemplate
41	tasks	medicationtasktemplate
42	tasks	symptomtasktemplate
44	tasks	assessmentquestion
48	tasks	assessmentresponse
49	tasks	symptomrating
50	tasks	teamtasktemplate
51	tasks	patienttasktemplate
21	plans	careplan
43	tasks	assessmenttask
46	tasks	medicationtask
47	tasks	patienttask
52	tasks	symptomtask
45	tasks	teamtask
53	plans	goalprogress
54	plans	goalcomment
55	tasks	vitaltasktemplate
56	tasks	vitaltask
57	tasks	vitalquestion
58	tasks	vitalresponse
59	sites	site
60	account	emailaddress
61	account	emailconfirmation
62	core	invitedemailtemplate
63	patients	reminderemail
64	patients	patientverificationcode
65	patients	potentialpatient
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 65, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2018-07-23 15:27:05.552856+00
2	contenttypes	0002_remove_content_type_name	2018-07-23 15:27:05.563347+00
3	auth	0001_initial	2018-07-23 15:27:05.610512+00
4	auth	0002_alter_permission_name_max_length	2018-07-23 15:27:05.617348+00
5	auth	0003_alter_user_email_max_length	2018-07-23 15:27:05.624146+00
6	auth	0004_alter_user_username_opts	2018-07-23 15:27:05.630762+00
7	auth	0005_alter_user_last_login_null	2018-07-23 15:27:05.637516+00
8	auth	0006_require_contenttypes_0002	2018-07-23 15:27:05.639509+00
9	auth	0007_alter_validators_add_error_messages	2018-07-23 15:27:05.646013+00
10	auth	0008_alter_user_username_max_length	2018-07-23 15:27:05.652758+00
11	accounts	0001_initial	2018-07-23 15:27:05.699753+00
12	accounts	0002_auto_20180723_0918	2018-07-23 15:27:05.708491+00
13	admin	0001_initial	2018-07-23 15:27:05.736336+00
14	admin	0002_logentry_remove_auto_add	2018-07-23 15:27:05.746171+00
15	auth	0009_alter_user_last_name_max_length	2018-07-23 15:27:05.755504+00
16	authtoken	0001_initial	2018-07-23 15:27:05.774029+00
17	authtoken	0002_auto_20160226_1747	2018-07-23 15:27:05.812523+00
18	core	0001_initial	2018-07-23 15:27:06.019789+00
19	patients	0001_initial	2018-07-23 15:27:06.227988+00
21	sessions	0001_initial	2018-07-23 15:27:06.4045+00
22	core	0002_auto_20180731_1612	2018-08-15 19:41:34.157752+00
23	core	0003_employeeprofile_status	2018-08-15 19:41:34.209571+00
24	patients	0002_patientmedication	2018-08-15 19:41:34.258881+00
31	patients	0003_remove_patientmedication_refills	2018-09-06 19:26:33.892149+00
33	core	0004_symptom	2018-09-11 09:39:58.440271+00
34	plans	0001_initial	2018-09-11 09:39:58.627054+00
35	tasks	0001_initial	2018-09-11 09:39:59.209862+00
36	tasks	0002_auto_20180910_1849	2018-09-11 09:39:59.445558+00
37	tasks	0003_assessmenttaskinstance_assessment_task_template	2018-09-11 09:39:59.501226+00
38	plans	0002_auto_20180912_2136	2018-09-13 16:55:46.26154+00
39	tasks	0004_auto_20180912_2136	2018-09-13 16:55:46.9358+00
40	tasks	0005_teamtask_status	2018-09-17 05:27:47.192517+00
41	patients	0004_patientprofile_emr_code	2018-09-17 19:24:13.257318+00
42	tasks	0006_auto_20180917_1316	2018-09-17 19:24:13.307724+00
43	tasks	0006_auto_20180917_2034	2018-09-18 19:14:17.241141+00
44	tasks	0007_auto_20180917_2040	2018-09-18 19:14:17.331305+00
45	tasks	0008_symptomtask_is_complete	2018-09-18 19:14:17.359579+00
46	tasks	0009_auto_20180917_2351	2018-09-18 19:14:17.41167+00
47	tasks	0010_merge_20180918_0017	2018-09-18 19:14:17.413802+00
48	tasks	0011_auto_20180918_2243	2018-09-20 20:17:41.957421+00
49	plans	0003_goal	2018-09-24 18:39:26.731603+00
50	plans	0004_goalprogress	2018-09-24 18:39:26.789853+00
51	plans	0005_goalcomment	2018-09-24 18:39:26.854111+00
52	plans	0003_careplantemplate_is_active	2018-09-24 18:39:26.873383+00
53	plans	0006_merge_20180921_0117	2018-09-24 18:39:26.875616+00
54	tasks	0012_vitaltasktemplate	2018-09-24 18:39:26.923775+00
55	tasks	0013_vitaltask	2018-09-24 18:39:26.975333+00
56	tasks	0014_vitalquestion	2018-09-24 18:39:27.026589+00
57	tasks	0015_vitalresponse	2018-09-24 18:39:27.080957+00
58	tasks	0016_auto_20180923_2247	2018-09-25 19:50:15.633419+00
59	tasks	0017_auto_20180924_0259	2018-09-25 19:50:15.691124+00
60	tasks	0018_auto_20180924_1939	2018-09-25 19:50:15.744976+00
61	plans	0007_auto_20180925_0148	2018-09-26 03:06:37.136595+00
62	tasks	0019_auto_20180925_1840	2018-09-26 03:06:37.145687+00
63	account	0001_initial	2018-10-05 20:16:14.153301+00
64	account	0002_email_max_length	2018-10-05 20:16:14.179006+00
65	accounts	0003_emailuser_time_zone	2018-10-05 20:16:14.219731+00
66	core	0005_invitedemailtemplate	2018-10-05 20:16:14.233164+00
67	core	0005_auto_20181002_0641	2018-10-05 20:16:14.24797+00
68	core	0006_merge_20181005_1359	2018-10-05 20:16:14.250121+00
69	patients	0005_reminderemail	2018-10-05 20:16:14.311843+00
70	patients	0005_auto_20181003_2138	2018-10-05 20:16:14.384826+00
71	patients	0006_merge_20181005_1359	2018-10-05 20:16:14.386979+00
72	plans	0008_goal_start_on_datetime	2018-10-05 20:16:14.399058+00
73	plans	0009_auto_20180927_0139	2018-10-05 20:16:58.938211+00
74	sites	0001_initial	2018-10-05 20:16:58.950473+00
75	sites	0002_alter_domain_unique	2018-10-05 20:16:58.963898+00
76	patients	0006_auto_20181004_1930	2018-10-08 07:16:12.786245+00
77	patients	0007_merge_20181005_2157	2018-10-08 07:16:12.788773+00
78	accounts	0004_emailuser_is_active	2018-10-08 20:34:39.420543+00
79	patients	0008_auto_20181008_0505	2018-10-09 16:54:16.339476+00
80	tasks	0020_auto_20181008_2207	2018-10-09 16:54:16.397535+00
81	plans	0010_careteammember_is_manager	2018-10-17 06:35:40.268298+00
82	plans	0011_auto_20181017_1335	2018-10-17 20:03:00.626456+00
83	patients	0009_auto_20181017_1820	2018-10-23 18:58:42.113655+00
84	patients	0010_remove_patientprofile_status	2018-10-23 18:58:42.147277+00
85	patients	0011_potentialpatient	2018-10-23 18:58:42.245648+00
86	patients	0012_auto_20181018_2200	2018-10-23 18:58:42.26998+00
87	patients	0013_patientprofile_last_app_use	2018-10-23 18:58:42.314496+00
88	tasks	0021_auto_20181020_0015	2018-10-23 18:58:42.381681+00
89	tasks	0022_auto_20181023_2045	2018-10-24 19:41:42.09836+00
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 89, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
78dhahazo8aeoo6xbe7j2omhklj1c8ft	Mjg3NmMyZjJlNTUwODcxOTg3NjM1NzcwZDI5NDVkMDMxOTRjMWQ4NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6ImE0YmQ1M2U0LTUxZDEtNGIxZi04ZDkyLTRkNzVlN2RmMmJkOCIsIl9hdXRoX3VzZXJfaGFzaCI6ImUyMTdjMjMwNDU2MGZlZTkwZjc3NGY2NzZjODVkOTZlZjM5ZTYzNTgifQ==	2018-08-06 15:27:55.941875+00
unwh9uottxhsx737aqs9ltkkd2bo970u	NTczNDZkZmFiN2NmN2MxODU5NTI0YWI5MWQyYmFkZTNmNTc2MGU0Njp7Il9hdXRoX3VzZXJfaWQiOiJhOTExMmEwNy0zMTUxLTRmNjEtYWM2ZC1jMWU3ZDJiZWNmZGYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImZlMzRlYjA4Y2UxYzE1ZDhkMjQ4NDMxYTBhZDkwODg2ODcyMzIxM2UifQ==	2018-08-07 15:11:04.745504+00
iw0d44fp18vdf8ixppkhq5nnp3rq3i5c	NTczNDZkZmFiN2NmN2MxODU5NTI0YWI5MWQyYmFkZTNmNTc2MGU0Njp7Il9hdXRoX3VzZXJfaWQiOiJhOTExMmEwNy0zMTUxLTRmNjEtYWM2ZC1jMWU3ZDJiZWNmZGYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImZlMzRlYjA4Y2UxYzE1ZDhkMjQ4NDMxYTBhZDkwODg2ODcyMzIxM2UifQ==	2018-08-08 23:28:52.146647+00
w0gboqfak9ir9cw4yvss8tku5dfpp7cx	NTczNDZkZmFiN2NmN2MxODU5NTI0YWI5MWQyYmFkZTNmNTc2MGU0Njp7Il9hdXRoX3VzZXJfaWQiOiJhOTExMmEwNy0zMTUxLTRmNjEtYWM2ZC1jMWU3ZDJiZWNmZGYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImZlMzRlYjA4Y2UxYzE1ZDhkMjQ4NDMxYTBhZDkwODg2ODcyMzIxM2UifQ==	2018-08-09 00:24:55.306089+00
4cmqgylg8trefz2tcl4gysielsqxsnfo	ZDViMWI1YWQxNjk3ZDBmOWFhODAzNTU0NjU4ZDFmZDlkZmJhNzNjYjp7Il9hdXRoX3VzZXJfaWQiOiJhNGJkNTNlNC01MWQxLTRiMWYtOGQ5Mi00ZDc1ZTdkZjJiZDgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImUyMTdjMjMwNDU2MGZlZTkwZjc3NGY2NzZjODVkOTZlZjM5ZTYzNTgifQ==	2018-08-20 17:43:16.737791+00
zdr0ngwio10atlfb8a3qmgvn1hz3la2w	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-08-21 15:32:57.024232+00
3dbmcppgoyyunn8rr8bmct7ahk0327w3	MGM3OTljMjM4ZGYwMDdiZDc0NjdlYzY1ODY3OWU5Njc4OTM0ODI0Mjp7Il9hdXRoX3VzZXJfaWQiOiJiZGEwYjQ4OS1iOTllLTQ1ZjYtOTNlMS0yN2RmYzY5NDJkYTkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjNhMTE2ZmYxYmIwZjlhYjJhOTA0YmFkYmQ0MDQ1NjJhZGRhOGEzZWMifQ==	2018-08-27 16:06:52.805821+00
z83rd6b3h3jwsgtlmwuk6ikkshwi78om	MGM3OTljMjM4ZGYwMDdiZDc0NjdlYzY1ODY3OWU5Njc4OTM0ODI0Mjp7Il9hdXRoX3VzZXJfaWQiOiJiZGEwYjQ4OS1iOTllLTQ1ZjYtOTNlMS0yN2RmYzY5NDJkYTkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjNhMTE2ZmYxYmIwZjlhYjJhOTA0YmFkYmQ0MDQ1NjJhZGRhOGEzZWMifQ==	2018-08-27 16:07:42.722286+00
j6d85lkq9po8fpxxr00z11z36pesxmfq	MWNjNmIwZTI4Mzk5NDljZmQ1NmRkODk4ZmExMjQwMThlMmY1Nzg0ZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjZhZmE0MWE0NjJjYmQzYzU4MjQ5ZDA0OTBkYmQxOGI2NDM1NzZlMmUiLCJfYXV0aF91c2VyX2lkIjoiODgxNjY1ZTktNjI1YS00ZmEzLTlkMzItYTY3MGZkZjA0YjRhIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQifQ==	2018-09-03 16:40:37.997395+00
ya78gupjdidv7n61bd77zosxquyyjjzf	ODRiZTRlMWE3ZDhhYmRjNWE4ZGJmNGYzZmI2Y2I2ZTAxZjJkNDNkMTp7Il9hdXRoX3VzZXJfaGFzaCI6ImUyMTdjMjMwNDU2MGZlZTkwZjc3NGY2NzZjODVkOTZlZjM5ZTYzNTgiLCJfYXV0aF91c2VyX2lkIjoiYTRiZDUzZTQtNTFkMS00YjFmLThkOTItNGQ3NWU3ZGYyYmQ4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQifQ==	2018-09-03 21:53:04.753165+00
vsngdb7pgw0dbvc778sfmpoeprzv5llq	OGU0MjE0ZWM0MTkyYWJjYWFhNmY1NTI5Y2Q4ODJjZjYxY2MyMjJjYjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjAyNDk3OGMyLWY5ZjgtNGVjNi04NzczLTVlZmFmOGYxM2VlYSIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-09-11 16:01:33.098673+00
r7olii6pj5y4sycatacdvaffgci715qf	NmY3NjVkYjc5M2E5MjhhNTY5NjExMzU3ODg4NDc0YjIxMDVkNzE4Yzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNTAyNWI1ZTJhNzQ5ODhlOTNiMDlhMWRhNjEwYmI4YjRkOGY0N2E4YyIsIl9hdXRoX3VzZXJfaWQiOiI2NjhhYjhmOC1iMGU5LTQ3ODgtOWFiZi04OWQ5OTdmMjkwYjgifQ==	2018-09-25 09:42:22.774059+00
whi4rscuhooemj99rcjqsjeri2s8ii0j	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-09-25 19:35:43.995602+00
xcv4v8uuru2ki6dbps1y4im9aokofzsb	MTNlM2Q1M2M2MDhlMmQ0OTE3OWNlYzYxMjFhMWRlYjRkNTYwOWM4MTp7Il9hdXRoX3VzZXJfaWQiOiI2NjhhYjhmOC1iMGU5LTQ3ODgtOWFiZi04OWQ5OTdmMjkwYjgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwMjViNWUyYTc0OTg4ZTkzYjA5YTFkYTYxMGJiOGI0ZDhmNDdhOGMifQ==	2018-09-25 20:01:04.588906+00
l9ysy81u4o3aumy3qpnrsec6f67306yq	NDg0ZjEyNDY5NmVjZDI0NjNhMTY4ZGZhYmJjNDFkODZjNmYzYTQ3Zjp7Il9hdXRoX3VzZXJfaWQiOiJiZDg2ZjRiOS05NTFhLTQ2N2MtOThkZC1mOWZiNTM1ZDI1NWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjM3ZGNlMDc0NDE1MTJlNDM5YzA4MjkyOTM0OGM3YTk3OTg2NzVhZGMifQ==	2018-10-01 20:23:29.203833+00
l5t9s4xi8mrwskof6mys55gsyf0g93al	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-10-02 17:06:52.911272+00
teshgjipubmkbrnp91jnh5x2z65t81a0	ZDViMWI1YWQxNjk3ZDBmOWFhODAzNTU0NjU4ZDFmZDlkZmJhNzNjYjp7Il9hdXRoX3VzZXJfaWQiOiJhNGJkNTNlNC01MWQxLTRiMWYtOGQ5Mi00ZDc1ZTdkZjJiZDgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImUyMTdjMjMwNDU2MGZlZTkwZjc3NGY2NzZjODVkOTZlZjM5ZTYzNTgifQ==	2018-10-02 20:14:52.163493+00
uas7dy7olx6w2d43wmsrw8plruzk58t1	MmYwYzdmYjFjMjlmYzNlNzQ0ZjUzNzI3NGFhMjg5MThiYzUyMjhjZjp7Il9hdXRoX3VzZXJfaWQiOiI0ZDU4ZjE2MS0yN2YzLTRmYmUtOTFiNS05MzBjNmI0ZTI5NTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjdhOTI3NjVkNTIxNmM1MzdiNTc5ZWRjZTEwNTEzNmFmZmY0YjA1ZTIifQ==	2018-10-03 01:30:35.145991+00
fqrc3iud8gsafzi8un3g8flcuhh7jx86	MTNlM2Q1M2M2MDhlMmQ0OTE3OWNlYzYxMjFhMWRlYjRkNTYwOWM4MTp7Il9hdXRoX3VzZXJfaWQiOiI2NjhhYjhmOC1iMGU5LTQ3ODgtOWFiZi04OWQ5OTdmMjkwYjgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwMjViNWUyYTc0OTg4ZTkzYjA5YTFkYTYxMGJiOGI0ZDhmNDdhOGMifQ==	2018-10-04 22:05:30.606967+00
wp4i17risx0kc8bm34cg6iiup12hwezk	MTNlM2Q1M2M2MDhlMmQ0OTE3OWNlYzYxMjFhMWRlYjRkNTYwOWM4MTp7Il9hdXRoX3VzZXJfaWQiOiI2NjhhYjhmOC1iMGU5LTQ3ODgtOWFiZi04OWQ5OTdmMjkwYjgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwMjViNWUyYTc0OTg4ZTkzYjA5YTFkYTYxMGJiOGI0ZDhmNDdhOGMifQ==	2018-10-09 02:59:59.231535+00
vsppx9huo376omiaaki4aok06b17x0pf	YTU0YmM3OWJiY2IwMGUyMjU1Y2FiYmYyZDg1MjQ4MDFkZmQwYzRjMzp7Il9hdXRoX3VzZXJfaWQiOiI2OTk4ZjVmMi00Mzk2LTRmOTUtOTI4MS0xMzY1MTQ0YzgwZWYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjZlNDdiYzc3ZmI3ZWM5NzRkOGZlNjU4YTFkYWU3ZWE3MGUxNjM5YzEifQ==	2018-10-09 06:36:27.335229+00
3te47hxroxhjvmbzmnaxnp87ystnk5r4	MTNlM2Q1M2M2MDhlMmQ0OTE3OWNlYzYxMjFhMWRlYjRkNTYwOWM4MTp7Il9hdXRoX3VzZXJfaWQiOiI2NjhhYjhmOC1iMGU5LTQ3ODgtOWFiZi04OWQ5OTdmMjkwYjgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwMjViNWUyYTc0OTg4ZTkzYjA5YTFkYTYxMGJiOGI0ZDhmNDdhOGMifQ==	2018-10-09 20:00:15.337384+00
gt7lyrysr22fnnh0vvggdwxagwu8dgow	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-10-23 16:56:01.177341+00
fbnew3lcoqftpyhwtc8vyafan6c2it6h	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-10-10 22:26:50.329273+00
xq6lhmggum513hw89nzxgf645mfe4qbg	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-10-16 19:56:00.706913+00
tc3vc7dutnkobuxn5lwet34a1rkb2z5c	MTNlM2Q1M2M2MDhlMmQ0OTE3OWNlYzYxMjFhMWRlYjRkNTYwOWM4MTp7Il9hdXRoX3VzZXJfaWQiOiI2NjhhYjhmOC1iMGU5LTQ3ODgtOWFiZi04OWQ5OTdmMjkwYjgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwMjViNWUyYTc0OTg4ZTkzYjA5YTFkYTYxMGJiOGI0ZDhmNDdhOGMifQ==	2018-10-24 22:14:52.988591+00
x1b1390nnhsw34tnqemtoblk1wvo8skq	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-10-25 17:19:58.758309+00
3d4wlm4njm0731z7e9jxpd71v70qy1fk	MmYwYzdmYjFjMjlmYzNlNzQ0ZjUzNzI3NGFhMjg5MThiYzUyMjhjZjp7Il9hdXRoX3VzZXJfaWQiOiI0ZDU4ZjE2MS0yN2YzLTRmYmUtOTFiNS05MzBjNmI0ZTI5NTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjdhOTI3NjVkNTIxNmM1MzdiNTc5ZWRjZTEwNTEzNmFmZmY0YjA1ZTIifQ==	2018-10-17 23:49:18.919162+00
4vm8jhqyvpfyx8cvlxailo3onfu5ggyi	MTNlM2Q1M2M2MDhlMmQ0OTE3OWNlYzYxMjFhMWRlYjRkNTYwOWM4MTp7Il9hdXRoX3VzZXJfaWQiOiI2NjhhYjhmOC1iMGU5LTQ3ODgtOWFiZi04OWQ5OTdmMjkwYjgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwMjViNWUyYTc0OTg4ZTkzYjA5YTFkYTYxMGJiOGI0ZDhmNDdhOGMifQ==	2018-10-18 22:17:28.974179+00
q7gqcvdrh9ekmx0tzh07o9flrolqb66m	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-10-30 21:32:25.420197+00
galjh40y6d6w77xy3hp73trqzgbgjj27	MzI4ODdlZDA0YjVlMjFlOWMwY2FlMzdmYjg4YzEyNWQxMjQ3ZDc2NDp7Il9hdXRoX3VzZXJfaWQiOiJhNGJkNTNlNC01MWQxLTRiMWYtOGQ5Mi00ZDc1ZTdkZjJiZDgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjZiYWJiNDUyMDdmNGI0YTEyNDMwZmMzNjA1ZjIzODhlMmY4MDA0OWMifQ==	2018-10-30 23:24:01.367688+00
ve5aezti1fkfwnb81xhmgqr20p0tp3sz	NzFkN2U3NjcxNjFhNzc4ZTBjNTAyMWRkNGE2NTZhNmUzMDg2MTc3Zjp7Il9hdXRoX3VzZXJfaWQiOiI4NmI5MjUxOC05YzJhLTRjYTgtYTQ3MS0yODYwNDczYzRiOWUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhkYmUwZmY0MjU3Yjg2YWE1MTZlYTE4YTY5Y2M3ZGIyY2IwYWZjZDIifQ==	2018-10-31 20:26:47.312516+00
jj0f0iv2b91p87ich7vdizre9ttqyjbi	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-11-07 20:17:45.915011+00
ywdp8try4u8a0xw9ixjhaxcryc15wlyq	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-11-15 20:33:05.089955+00
od0paqh80mt48h1ca1gcwvr1zqtqs73b	NGI1ZDA2YzJlYmM4YzRkNTYxYTg0MzQ1NDNmNmNjNDNmYTVhYWVmMTp7Il9hdXRoX3VzZXJfaWQiOiIwMjQ5NzhjMi1mOWY4LTRlYzYtODc3My01ZWZhZjhmMTNlZWEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImQ5NjQyYWNiYzI3MDkwMGMzNzBlOTVjNjVmNGRkZjJhY2ZiZDgzNzYifQ==	2018-11-20 23:20:16.472109+00
onmew9eeam24rwhgsp8b7gf7xf4n514e	MzI4ODdlZDA0YjVlMjFlOWMwY2FlMzdmYjg4YzEyNWQxMjQ3ZDc2NDp7Il9hdXRoX3VzZXJfaWQiOiJhNGJkNTNlNC01MWQxLTRiMWYtOGQ5Mi00ZDc1ZTdkZjJiZDgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjZiYWJiNDUyMDdmNGI0YTEyNDMwZmMzNjA1ZjIzODhlMmY4MDA0OWMifQ==	2018-11-24 18:40:34.418169+00
xngmlds0cwmzxjs2v8qf88zr6tbf8vw9	MzI4ODdlZDA0YjVlMjFlOWMwY2FlMzdmYjg4YzEyNWQxMjQ3ZDc2NDp7Il9hdXRoX3VzZXJfaWQiOiJhNGJkNTNlNC01MWQxLTRiMWYtOGQ5Mi00ZDc1ZTdkZjJiZDgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjZiYWJiNDUyMDdmNGI0YTEyNDMwZmMzNjA1ZjIzODhlMmY4MDA0OWMifQ==	2018-11-25 05:49:05.288253+00
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.django_site (id, domain, name) FROM stdin;
1	careadopt.izeni.net	careadopt.izeni.net
\.


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Data for Name: patients_patientdiagnosis; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.patients_patientdiagnosis (id, type, date_identified, diagnosing_practitioner, facility, diagnosis_id, patient_id) FROM stdin;
1e986c82-0fcc-494f-b1a5-b9d78be4964c	Chronic	2018-07-17	Dr. Nick Riviera	Ogden Clinic	ece37c05-48f9-45d2-8e81-c533deb924b5	6b35be7c-427f-40bd-977e-468746e946f2
3a7efca6-f5f7-49b8-a420-4e233f658bb1	Test	2018-08-13	\N	\N	98ffe758-e7d0-4539-a213-e4781e6218ee	ca3be682-4ee3-4f4f-8c11-b9c9f71f63be
\.


--
-- Data for Name: patients_patientmedication; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.patients_patientmedication (id, dose_mg, date_prescribed, duration_days, instructions, medication_id, patient_id, prescribing_practitioner_id) FROM stdin;
6e992289-11a6-40e7-806b-1815d71e67f6	10	2018-08-22	7	Take twice orally with water	3ee1039a-0dd6-4dcc-b31b-cf3dc61de361	6b35be7c-427f-40bd-977e-468746e946f2	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48
157a8f16-73d8-473f-a4a7-bda6e3102af7	10	2018-08-22	7	Take twice orally with water	3ee1039a-0dd6-4dcc-b31b-cf3dc61de361	ca3be682-4ee3-4f4f-8c11-b9c9f71f63be	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48
d49ed3a2-3625-4bf3-bd91-10e2dec10cc3	10	2018-09-11	21	Take with food.	3ee1039a-0dd6-4dcc-b31b-cf3dc61de361	78d5472b-32d4-4b15-8dd1-f14a65070da4	68523cec-50cb-4510-9508-99983fb0c8de
55137693-62f6-48f9-a6e1-14c6239323a1	10	2018-09-11	21	Take with food.	3ee1039a-0dd6-4dcc-b31b-cf3dc61de361	83437bc8-ac13-47f7-a1fd-727fc4d40b8d	68523cec-50cb-4510-9508-99983fb0c8de
c72d3ad9-e3a5-4d42-adf2-1a8a229b4546	10	2018-10-17	14	Take with food.	3ee1039a-0dd6-4dcc-b31b-cf3dc61de361	b310af7d-67df-4e4c-a34e-154b25b057ea	68523cec-50cb-4510-9508-99983fb0c8de
\.


--
-- Data for Name: patients_patientprocedure; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.patients_patientprocedure (id, date_of_procedure, attending_practitioner, facility, patient_id, procedure_id) FROM stdin;
f51fc974-284c-4ae8-b3a8-759416116496	2018-08-09	Dr. Nick Riviera	Ogden Clinic	6b35be7c-427f-40bd-977e-468746e946f2	54d366af-9ae6-45fe-acac-a3f5a45b9bf0
\.


--
-- Data for Name: patients_patientprofile; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.patients_patientprofile (created, modified, id, facility_id, user_id, emr_code, message_for_day_id, is_active, is_invited, last_app_use) FROM stdin;
2018-07-27 16:17:48.328011+00	2018-08-30 20:26:22.881538+00	83437bc8-ac13-47f7-a1fd-727fc4d40b8d	dcc71bd8-31cf-4e98-a26c-cac02021f5f6	881665e9-625a-4fa3-9d32-a670fdf04b4a	\N	\N	f	f	2018-10-23 18:58:42.296118+00
2018-08-13 16:17:07.199206+00	2018-08-30 20:26:38.396741+00	ca3be682-4ee3-4f4f-8c11-b9c9f71f63be	07aa1282-18a2-4e36-bba9-3d5581402d6d	bda0b489-b99e-45f6-93e1-27dfc6942da9	\N	\N	f	f	2018-10-23 18:58:42.296118+00
2018-09-14 00:25:19.570871+00	2018-09-14 00:25:19.570892+00	ebf7cce4-712f-4583-a398-e77c7686115b	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3	5794fb47-d466-4686-b467-fb6c0124a712	\N	\N	f	f	2018-10-23 18:58:42.296118+00
2018-10-17 06:39:46.614922+00	2018-10-17 06:39:46.614954+00	b310af7d-67df-4e4c-a34e-154b25b057ea	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3	86b92518-9c2a-4ca8-a471-2860473c4b9e	22222	\N	f	f	2018-10-24 19:44:52.182661+00
2018-08-06 17:55:06.918282+00	2018-08-30 20:26:18.650514+00	6b35be7c-427f-40bd-977e-468746e946f2	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3	024978c2-f9f8-4ec6-8773-5efaf8f13eea	\N	\N	f	f	2018-11-09 23:47:56.622932+00
2018-07-23 15:39:06.677467+00	2018-08-30 20:26:34.286161+00	78d5472b-32d4-4b15-8dd1-f14a65070da4	e55dbc82-66a3-4441-b8b0-8f7f42a1b2f3	668ab8f8-b0e9-4788-9abf-89d997f290b8	\N	\N	f	f	2018-10-24 20:16:55.795394+00
\.


--
-- Data for Name: patients_patientprofile_diagnosis; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.patients_patientprofile_diagnosis (id, patientprofile_id, patientdiagnosis_id) FROM stdin;
\.


--
-- Name: patients_patientprofile_diagnosis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.patients_patientprofile_diagnosis_id_seq', 2, true);


--
-- Data for Name: patients_patientverificationcode; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.patients_patientverificationcode (created, modified, id, code, patient_id) FROM stdin;
2018-10-17 06:39:46.618276+00	2018-10-17 06:39:46.618295+00	98c6ce33-015c-4a5c-9575-0a4a0d7f3eb9	B4VP79	b310af7d-67df-4e4c-a34e-154b25b057ea
\.


--
-- Data for Name: patients_potentialpatient; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.patients_potentialpatient (created, modified, id, first_name, last_name, care_plan, phone, patient_profile_id) FROM stdin;
2018-10-25 18:03:42.759459+00	2018-10-25 18:03:42.759476+00	4b986fdb-14d3-4615-93fa-fa153f69a96c	Jordan	Price	Depression	888-888-8888	\N
\.


--
-- Data for Name: patients_potentialpatient_facility; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.patients_potentialpatient_facility (id, potentialpatient_id, facility_id) FROM stdin;
\.


--
-- Name: patients_potentialpatient_facility_id_seq; Type: SEQUENCE SET; Schema: public; Owner: care_adopt_backend
--

SELECT pg_catalog.setval('public.patients_potentialpatient_facility_id_seq', 1, false);


--
-- Data for Name: patients_problemarea; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.patients_problemarea (created, modified, id, date_identified, name, description, identified_by_id, patient_id) FROM stdin;
2018-08-07 15:44:36.516264+00	2018-08-07 15:44:36.516285+00	2a72ea9c-05f2-4c14-a2e3-c2e6fddee4b8	2018-08-07	Lupis	It's Lupis	68523cec-50cb-4510-9508-99983fb0c8de	6b35be7c-427f-40bd-977e-468746e946f2
2018-08-07 15:45:01.706491+00	2018-08-07 15:45:01.70652+00	04535005-0e14-4639-8604-550597bb66cd	2018-08-01	Gonorrhea	It burns	68523cec-50cb-4510-9508-99983fb0c8de	6b35be7c-427f-40bd-977e-468746e946f2
2018-09-26 19:35:19.276227+00	2018-09-26 19:35:19.276247+00	df047e01-541f-41cc-8da6-036edae237da	2018-09-26	Terrible Problem Area	It's so bad that it needed to be defined	68523cec-50cb-4510-9508-99983fb0c8de	78d5472b-32d4-4b15-8dd1-f14a65070da4
\.


--
-- Data for Name: patients_reminderemail; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.patients_reminderemail (created, modified, id, subject, message, patient_id) FROM stdin;
\.


--
-- Data for Name: plans_careplan; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.plans_careplan (created, modified, id, patient_id, plan_template_id) FROM stdin;
2018-10-05 20:21:38.730912+00	2018-10-05 20:21:38.730932+00	fdb25787-150f-4117-a757-b1cd399b98f3	6b35be7c-427f-40bd-977e-468746e946f2	719563fb-6394-47b8-89e0-3f6f4fad9c9f
2018-10-05 20:21:59.135179+00	2018-10-05 20:21:59.135197+00	141ed317-4a19-4a30-b245-4909bf6a9767	6b35be7c-427f-40bd-977e-468746e946f2	b1754551-afc9-4eb2-9b6e-dfbc3e373b14
2018-10-16 21:15:58.642731+00	2018-10-16 21:15:58.642749+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	78d5472b-32d4-4b15-8dd1-f14a65070da4	719563fb-6394-47b8-89e0-3f6f4fad9c9f
2018-10-17 07:04:53.415843+00	2018-10-17 07:04:53.41586+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	b310af7d-67df-4e4c-a34e-154b25b057ea	719563fb-6394-47b8-89e0-3f6f4fad9c9f
\.


--
-- Data for Name: plans_careplantemplate; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.plans_careplantemplate (created, modified, id, name, type, duration_weeks, is_active) FROM stdin;
2018-09-11 09:46:28.886961+00	2018-09-11 09:46:28.886984+00	719563fb-6394-47b8-89e0-3f6f4fad9c9f	Depression	rpm	6	t
2018-09-21 08:21:56.978302+00	2018-09-21 08:21:56.978339+00	b1754551-afc9-4eb2-9b6e-dfbc3e373b14	Test Plan Depression	ccm	6	t
\.


--
-- Data for Name: plans_careteammember; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.plans_careteammember (id, employee_profile_id, plan_id, role_id, is_manager) FROM stdin;
d140a271-3f1f-494e-8e2e-e86bdf84e743	68523cec-50cb-4510-9508-99983fb0c8de	fdb25787-150f-4117-a757-b1cd399b98f3	f706665f-c518-4bd5-ad31-68c3d40fad8a	f
4ba0968c-06bc-446c-90e6-f3166927c7ad	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	fdb25787-150f-4117-a757-b1cd399b98f3	e78afb29-e874-424e-92e7-6245f8190beb	f
abacd08a-4147-408b-b925-0a8339703488	68523cec-50cb-4510-9508-99983fb0c8de	a52bdf43-4e23-4d89-a931-cb36e6979a12	f706665f-c518-4bd5-ad31-68c3d40fad8a	f
bc9fd625-da47-4a21-aece-0754d9b87865	ee2b1ce2-f0d2-4247-8b94-fe3fd7b25f48	a52bdf43-4e23-4d89-a931-cb36e6979a12	e78afb29-e874-424e-92e7-6245f8190beb	f
\.


--
-- Data for Name: plans_goal; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.plans_goal (created, modified, id, goal_template_id, plan_id, start_on_datetime) FROM stdin;
2018-10-05 20:21:38.733649+00	2018-10-05 20:21:38.733668+00	4273c553-5602-4d8f-a42f-f2c03861ad16	f5b4a640-5edc-4f02-b10b-e39f54df9c4d	fdb25787-150f-4117-a757-b1cd399b98f3	2018-10-05 20:21:38.733359+00
2018-10-16 21:15:58.644566+00	2018-10-16 21:15:58.644582+00	e13b017c-4f87-4106-86d7-832d0c09e722	f5b4a640-5edc-4f02-b10b-e39f54df9c4d	a52bdf43-4e23-4d89-a931-cb36e6979a12	2018-10-16 21:15:58.644321+00
2018-10-17 07:04:53.417718+00	2018-10-17 07:04:53.417734+00	4f4e1df1-2e72-40f5-aefc-33c9e8904aa6	f5b4a640-5edc-4f02-b10b-e39f54df9c4d	c222e159-26f4-4bd6-9ea5-863f0cb0df71	2018-10-17 07:04:53.417488+00
\.


--
-- Data for Name: plans_goalcomment; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.plans_goalcomment (created, modified, id, content, goal_id, user_id) FROM stdin;
2018-10-16 21:29:59.130507+00	2018-10-16 21:29:59.130525+00	cf4d71f8-4b61-4522-a606-6b98db9c7c99	I'm commenting on my goal	4273c553-5602-4d8f-a42f-f2c03861ad16	024978c2-f9f8-4ec6-8773-5efaf8f13eea
2018-10-16 21:29:44.794101+00	2018-10-16 21:33:27.283426+00	a74ec5fd-51e8-40d8-92fe-c400fe206496	I'm commenting on your goal	4273c553-5602-4d8f-a42f-f2c03861ad16	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
2018-10-17 07:05:22.366614+00	2018-10-17 07:05:22.366633+00	570e5a30-f150-453e-8397-8ba6b17208c6	Test	4f4e1df1-2e72-40f5-aefc-33c9e8904aa6	86b92518-9c2a-4ca8-a471-2860473c4b9e
2018-10-17 07:05:30.702311+00	2018-10-17 07:05:30.702328+00	3086bc89-41ff-4d31-8b81-399ab5a7c49a	Test	4f4e1df1-2e72-40f5-aefc-33c9e8904aa6	a4bd53e4-51d1-4b1f-8d92-4d75e7df2bd8
2018-11-09 23:22:29.467926+00	2018-11-09 23:22:29.467947+00	024220fe-f5ff-4d28-aa43-52e629f7ff03	Hey, this is working!	4273c553-5602-4d8f-a42f-f2c03861ad16	024978c2-f9f8-4ec6-8773-5efaf8f13eea
2018-11-09 23:39:12.192775+00	2018-11-09 23:39:12.192801+00	56f892b4-1884-49f5-b9ad-8a408c75b9c7	Wow! I'm impressed!	4273c553-5602-4d8f-a42f-f2c03861ad16	024978c2-f9f8-4ec6-8773-5efaf8f13eea
2018-11-09 23:42:48.599608+00	2018-11-09 23:42:48.599632+00	3a9a2b2b-3b3d-4178-b4f8-8755dc647bdf	Sending another comment	4273c553-5602-4d8f-a42f-f2c03861ad16	024978c2-f9f8-4ec6-8773-5efaf8f13eea
2018-11-09 23:48:45.666061+00	2018-11-09 23:48:45.666086+00	59f3e0ae-e7bf-4b16-94f3-986e933b4210	blah blah blah	4273c553-5602-4d8f-a42f-f2c03861ad16	024978c2-f9f8-4ec6-8773-5efaf8f13eea
2018-11-09 23:51:11.961+00	2018-11-09 23:51:11.961026+00	f2a17c2b-c3ca-463a-b7c7-4bac6f4a297c	again again	4273c553-5602-4d8f-a42f-f2c03861ad16	024978c2-f9f8-4ec6-8773-5efaf8f13eea
\.


--
-- Data for Name: plans_goalprogress; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.plans_goalprogress (created, modified, id, rating, goal_id) FROM stdin;
2018-10-16 21:26:33.894824+00	2018-10-16 21:26:33.894844+00	7360410a-a370-4a02-afe3-f7a755315cea	2	4273c553-5602-4d8f-a42f-f2c03861ad16
2018-10-17 07:05:09.873934+00	2018-10-17 07:05:59.675194+00	c1531990-8062-468d-9b10-575a0004547c	1	4f4e1df1-2e72-40f5-aefc-33c9e8904aa6
\.


--
-- Data for Name: plans_goaltemplate; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.plans_goaltemplate (id, name, description, focus, start_on_day, duration_weeks, plan_template_id) FROM stdin;
f5b4a640-5edc-4f02-b10b-e39f54df9c4d	Manage Depression Symptoms	Manage Depression Symptoms	Manage Depression Symptoms	0	-1	719563fb-6394-47b8-89e0-3f6f4fad9c9f
\.


--
-- Data for Name: plans_infomessage; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.plans_infomessage (id, text, queue_id) FROM stdin;
3f16806b-85e1-4cbf-a143-5cbf2ad2d0a7	It mostly comes at night... mostly	8bd270e2-bd11-45db-9167-d4b9c9a07e19
\.


--
-- Data for Name: plans_infomessagequeue; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.plans_infomessagequeue (created, modified, id, name, type, plan_template_id) FROM stdin;
2018-09-11 09:47:27.548515+00	2018-09-11 09:47:31.7149+00	8bd270e2-bd11-45db-9167-d4b9c9a07e19	Depression Support Messages	support	719563fb-6394-47b8-89e0-3f6f4fad9c9f
\.


--
-- Data for Name: plans_planconsent; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.plans_planconsent (created, modified, id, verbal_consent, discussed_co_pay, seen_within_year, will_use_mobile_app, will_interact_with_team, will_complete_tasks, plan_id) FROM stdin;
2018-10-16 21:16:33.508841+00	2018-10-16 21:16:33.508869+00	cffbe6b3-3c7a-44a0-93b2-7abdfed5fdf8	t	t	t	t	t	t	a52bdf43-4e23-4d89-a931-cb36e6979a12
2018-10-16 21:16:40.887582+00	2018-10-16 21:16:40.887602+00	f3deb40c-5f67-4c70-acd6-2278b441e0fa	t	t	t	t	t	t	fdb25787-150f-4117-a757-b1cd399b98f3
\.


--
-- Data for Name: tasks_assessmentquestion; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_assessmentquestion (id, prompt, worst_label, best_label, assessment_task_template_id) FROM stdin;
78447557-fd62-441d-a87b-0569347f401b	Rate your happiness	Very Sad	Very Happy	9a67cb3a-debc-4c7a-ba45-5bb073db776f
3e817d57-99a3-424a-80b0-01b102faf6df	How are you feeling physically?	Awful	Great	9a67cb3a-debc-4c7a-ba45-5bb073db776f
\.


--
-- Data for Name: tasks_assessmentresponse; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_assessmentresponse (id, rating, assessment_question_id, assessment_task_id) FROM stdin;
6ce0c56e-eb0f-4c69-a1a8-4e5070141efd	3	3e817d57-99a3-424a-80b0-01b102faf6df	cf468975-e638-4cab-abb2-1144233b9c1d
c180a54c-4978-4e17-8cd7-8b4ec4623c07	3	78447557-fd62-441d-a87b-0569347f401b	cf468975-e638-4cab-abb2-1144233b9c1d
7bf8a3d2-9988-4e76-9536-fa1e1cf8e680	4	3e817d57-99a3-424a-80b0-01b102faf6df	cf468975-e638-4cab-abb2-1144233b9c1d
54602131-68b5-4755-b522-64535d165a7e	4	78447557-fd62-441d-a87b-0569347f401b	cf468975-e638-4cab-abb2-1144233b9c1d
68ed309e-0912-4a50-b93a-153a4774be24	4	3e817d57-99a3-424a-80b0-01b102faf6df	cf468975-e638-4cab-abb2-1144233b9c1d
0c60f023-a215-4c72-812b-64d552082065	4	78447557-fd62-441d-a87b-0569347f401b	cf468975-e638-4cab-abb2-1144233b9c1d
1b51e21b-0a34-45fa-9871-184b249d314b	4	3e817d57-99a3-424a-80b0-01b102faf6df	cf468975-e638-4cab-abb2-1144233b9c1d
8b6a4bb7-51c5-48a2-a412-d6ed253570e3	4	78447557-fd62-441d-a87b-0569347f401b	cf468975-e638-4cab-abb2-1144233b9c1d
ae94389a-8781-45c5-9660-d64c78d2b570	3	3e817d57-99a3-424a-80b0-01b102faf6df	2192ff41-3679-4c4e-951c-e22ccff33bc2
65738a51-e33a-4969-8873-b5e42ff719c0	3	78447557-fd62-441d-a87b-0569347f401b	2192ff41-3679-4c4e-951c-e22ccff33bc2
0224e87b-50bd-415a-81f0-1c53ceac211c	5	78447557-fd62-441d-a87b-0569347f401b	6fae57df-e845-4ca8-b179-3304ce393675
804e659a-0fd1-466a-9c15-c09d0b9cc16c	4	3e817d57-99a3-424a-80b0-01b102faf6df	6fae57df-e845-4ca8-b179-3304ce393675
bf7b1fbf-9de9-483c-91a4-22e6df3880e0	4	78447557-fd62-441d-a87b-0569347f401b	c894932a-818e-4232-800b-0867e3a839d8
9b35f2f5-c100-4885-84ab-69b8f2ad7057	4	3e817d57-99a3-424a-80b0-01b102faf6df	c894932a-818e-4232-800b-0867e3a839d8
4d42ca4a-a2bd-4061-bdad-20a491de8b4d	3	78447557-fd62-441d-a87b-0569347f401b	8e6c7ee1-5668-4fd3-a8cc-7dfe7d141d35
71517bc1-fec8-4ac5-b644-4ecdab1964db	4	3e817d57-99a3-424a-80b0-01b102faf6df	8e6c7ee1-5668-4fd3-a8cc-7dfe7d141d35
fb30d79e-9e82-44d4-92b3-9bf5a52e6807	4	78447557-fd62-441d-a87b-0569347f401b	ca66ea13-74d5-486a-8a33-985dc98dd0c3
c614e5a9-9898-473f-a29e-bac469a51c61	5	3e817d57-99a3-424a-80b0-01b102faf6df	ca66ea13-74d5-486a-8a33-985dc98dd0c3
\.


--
-- Data for Name: tasks_assessmenttask; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_assessmenttask (id, appear_datetime, due_datetime, comments, plan_id, assessment_task_template_id, is_complete) FROM stdin;
dfa90271-fa48-4c31-a5f8-f60b90993db1	2018-10-05 09:00:00+00	2018-10-05 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
140e4e33-af31-4ab3-8cd6-20794213e0bd	2018-10-06 09:00:00+00	2018-10-06 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
d4577d3b-8c92-47d5-a3de-5cc3761a5e32	2018-10-07 09:00:00+00	2018-10-07 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
101511b1-78dc-45ea-b6f5-b01033aaa64c	2018-10-08 09:00:00+00	2018-10-08 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
3def21c1-cab8-44b4-b872-9ecffaf88887	2018-10-09 09:00:00+00	2018-10-09 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
66a61a33-4dfc-4810-ae07-e7d1dba54dcf	2018-10-17 09:00:00+00	2018-10-17 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
74040383-703b-4b4b-9c68-11f2aefe9d49	2018-10-11 09:00:00+00	2018-10-11 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
326d7144-9825-4264-98e9-986a5a2d7412	2018-10-12 09:00:00+00	2018-10-12 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
6310d811-5f3a-491e-9ee9-3a893fde790b	2018-10-13 09:00:00+00	2018-10-13 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
558292f6-785c-474e-b5c6-9a430493af27	2018-10-14 09:00:00+00	2018-10-14 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
053cc534-c76c-4c62-a4d7-87ae02bbc11a	2018-10-15 09:00:00+00	2018-10-15 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
d4358870-0b7d-4226-a583-5101357fd6b6	2018-10-16 09:00:00+00	2018-10-16 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
3422ef37-0dc8-4921-b9e1-12c6b604c18c	2018-10-17 09:00:00+00	2018-10-17 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
ef94c588-fb02-43b7-ac13-137b156a825a	2018-10-18 09:00:00+00	2018-10-18 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
47632dc9-098e-4d49-9151-b293b51b0e97	2018-10-19 09:00:00+00	2018-10-19 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
acc0f380-1af7-42a0-a66f-fdc68d94fb0b	2018-10-20 09:00:00+00	2018-10-20 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
228c7a58-f0c6-4e22-a0d4-53a6af6c8aa9	2018-10-21 09:00:00+00	2018-10-21 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
ba56d86d-a7f6-4acf-a92f-6d065fb0c571	2018-10-22 09:00:00+00	2018-10-22 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
e25e38f2-92d6-4262-aa6c-1e627f50542b	2018-10-24 09:00:00+00	2018-10-24 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
932123fe-c973-4faf-a352-046395a82d12	2018-10-25 09:00:00+00	2018-10-25 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
1523098f-f76c-495e-b2e1-67dce00eedcd	2018-10-26 09:00:00+00	2018-10-26 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
bd7e4d16-a1c9-48dd-8e13-0ccc9b02131e	2018-10-27 09:00:00+00	2018-10-27 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
8a8afff2-6992-447f-879d-57c2daabbd61	2018-10-28 09:00:00+00	2018-10-28 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
ead32906-f9e7-49ea-b194-8aaa432c216f	2018-10-29 09:00:00+00	2018-10-29 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
db977cc5-6b2a-44ce-a2e0-a9da8d0c83cc	2018-10-30 09:00:00+00	2018-10-30 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
203bfa98-a576-425a-8950-b8549a4c4765	2018-10-31 09:00:00+00	2018-10-31 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
90dee884-eae4-474e-9c88-d6f5e1a3670e	2018-11-01 09:00:00+00	2018-11-01 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
60bd16be-0a47-4b2b-aa2e-ff622f67a359	2018-11-02 09:00:00+00	2018-11-02 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
a3eca5fc-41d2-49ce-a67d-4d7b97261d45	2018-11-03 09:00:00+00	2018-11-03 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
bf75002b-849e-4a36-8c82-484775e6d000	2018-11-04 09:00:00+00	2018-11-04 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
b97be50c-e1c3-421c-8380-563c66b45a3f	2018-11-05 09:00:00+00	2018-11-05 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
68908a89-d09a-4def-9aa1-aecc51b0ffe1	2018-11-06 09:00:00+00	2018-11-06 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
78728e7c-e20a-4c35-bdf4-8c0b4cb7f767	2018-11-07 09:00:00+00	2018-11-07 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
d5761a99-bc8b-4a55-84ff-ee39524e3606	2018-11-08 09:00:00+00	2018-11-08 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
336c7dfa-6a6d-4634-b551-fdb99b833332	2018-11-09 09:00:00+00	2018-11-09 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
3ba3051f-ba84-45f7-b023-239ab372178c	2018-11-10 09:00:00+00	2018-11-10 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
144f3b88-cf29-4bab-a6d6-ea33d69d1f51	2018-11-11 09:00:00+00	2018-11-11 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
43128001-2aed-4ad8-80ae-3c683a8924b0	2018-11-12 09:00:00+00	2018-11-12 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
37f1db20-ed39-4833-845d-4e8e58b8a787	2018-11-13 09:00:00+00	2018-11-13 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
699b6843-0266-4242-b839-1a80238cdd92	2018-11-14 09:00:00+00	2018-11-14 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
617bd1c9-38ae-417e-9346-abfc4906d308	2018-11-15 09:00:00+00	2018-11-15 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
217f8b75-559c-4679-bb6b-8b37cd4b05f0	2018-11-16 09:00:00+00	2018-11-16 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
1d16c605-27ef-4efa-abb1-cb3ffade8acd	2018-10-18 09:00:00+00	2018-10-18 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
52913c2a-c54e-40bb-81c6-cacf1d41f61f	2018-10-19 09:00:00+00	2018-10-19 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
49d38f9c-9c38-4c06-beab-7320ad97b8f5	2018-10-20 09:00:00+00	2018-10-20 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
14442d8e-54f8-468a-b549-6c510c437717	2018-10-21 09:00:00+00	2018-10-21 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
4d31a227-b3d4-4ceb-8e87-d952eb94401b	2018-10-22 09:00:00+00	2018-10-22 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
661a82a8-7798-49b5-a499-54902a33efc2	2018-10-23 09:00:00+00	2018-10-23 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
fb13db1b-a664-4fae-a416-70a6c29976b7	2018-10-24 09:00:00+00	2018-10-24 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
62c06b49-923b-4093-a9ed-a5fcff6d28b4	2018-10-25 09:00:00+00	2018-10-25 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
924e0586-d59e-43ba-a40b-ef784fcaaf68	2018-10-26 09:00:00+00	2018-10-26 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
06002f87-b95d-4f95-8cd6-ea744c47e5ab	2018-10-27 09:00:00+00	2018-10-27 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
49c61a44-2c96-4562-9fac-78576d9814c6	2018-10-28 09:00:00+00	2018-10-28 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
84890b68-8e38-4c22-9cb0-6bdc8689e771	2018-10-29 09:00:00+00	2018-10-29 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
2c623a05-9384-49e2-b223-49eaf3bf1faf	2018-10-30 09:00:00+00	2018-10-30 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
70d3e662-6009-4c5a-a401-4d7a3c918840	2018-10-31 09:00:00+00	2018-10-31 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
d09dc2a4-2f58-4bca-b5ff-17a8f1b34cc9	2018-11-01 09:00:00+00	2018-11-01 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
eb112171-840a-4ab4-a961-4b8440673ae2	2018-11-02 09:00:00+00	2018-11-02 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
9586fae5-7e0b-41b1-a5c5-e420bd006270	2018-11-03 09:00:00+00	2018-11-03 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
48140214-bcee-4eab-8f5f-0bf27eae6e8e	2018-11-04 09:00:00+00	2018-11-04 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
e5a33e3c-de75-431a-b08f-8d9ec8e46810	2018-11-05 09:00:00+00	2018-11-05 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
fc127f25-2503-4934-9255-65465bcf356f	2018-11-06 09:00:00+00	2018-11-06 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
47ba8d06-9192-43ae-a060-87e1869a2317	2018-11-07 09:00:00+00	2018-11-07 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
82a1bd69-88d5-483e-a4b9-5a1268875360	2018-11-08 09:00:00+00	2018-11-08 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
d0bd6e0f-7532-43da-81c7-d980d97e3936	2018-11-09 09:00:00+00	2018-11-09 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
353c461b-07ed-449d-94a7-1525006bbeaf	2018-11-10 09:00:00+00	2018-11-10 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
f4f515b0-356e-4e7d-b3ff-5b95017e73a0	2018-11-11 09:00:00+00	2018-11-11 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
2609101c-86ae-492b-b6f7-01f6585aa924	2018-11-12 09:00:00+00	2018-11-12 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
b43c5aee-c8e7-46be-b94b-ec4921dbb83f	2018-11-13 09:00:00+00	2018-11-13 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
244cb4e1-1336-4587-95fb-2ccc1b211c88	2018-11-14 09:00:00+00	2018-11-14 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
8dd9d1bc-084d-4695-ac36-84671beb84cc	2018-11-15 09:00:00+00	2018-11-15 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
057210d7-470b-4bdf-865e-6b622535f1c4	2018-11-16 09:00:00+00	2018-11-16 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
e6eff1f8-da51-4ea4-99fc-94792d5c1214	2018-11-17 09:00:00+00	2018-11-17 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
ca35edd6-22f1-4746-a734-f39f7f93b9b6	2018-11-18 09:00:00+00	2018-11-18 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
dd584316-4ee2-45d0-ae1b-b0f19d41e8ff	2018-11-19 09:00:00+00	2018-11-19 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
0f0de828-89d0-435a-bb12-c0c70c309481	2018-11-20 09:00:00+00	2018-11-20 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
86bb00ff-9f41-4c97-a9e5-260b9853ae53	2018-11-21 09:00:00+00	2018-11-21 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
ca595fe1-55b2-4623-9fa1-f1c46f26de4d	2018-11-22 09:00:00+00	2018-11-22 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
b40c8b51-09e8-460b-bc8f-b9d69a301b5c	2018-11-23 09:00:00+00	2018-11-23 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
f05d6789-596c-40b3-8509-ab15f8b630da	2018-11-24 09:00:00+00	2018-11-24 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
a40d5c6c-ca6c-4b5e-ad45-a4db3b4db0fd	2018-11-25 09:00:00+00	2018-11-25 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
aa3e4638-dd80-47e7-b7b0-e71bf04bf067	2018-11-26 09:00:00+00	2018-11-26 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
9bd02341-5512-49ec-a4b8-1a87b7b95cb8	2018-11-27 09:00:00+00	2018-11-27 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
be319886-2874-4715-b557-243167043c68	2018-11-28 09:00:00+00	2018-11-28 17:00:00+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
2192ff41-3679-4c4e-951c-e22ccff33bc2	2018-10-23 09:00:00+00	2018-10-23 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	t
6fae57df-e845-4ca8-b179-3304ce393675	2018-10-16 09:00:00+00	2018-10-16 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	t
c894932a-818e-4232-800b-0867e3a839d8	2018-10-17 09:00:00+00	2018-10-17 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	t
cf468975-e638-4cab-abb2-1144233b9c1d	2018-10-10 09:00:00+00	2018-10-10 17:00:00+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	9a67cb3a-debc-4c7a-ba45-5bb073db776f	t
fe4b0eb3-bd68-4bdb-8eac-823484b362ad	2018-10-19 09:00:00+00	2018-10-19 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
b33b77a7-86a8-4440-9b23-43afda44726f	2018-10-20 09:00:00+00	2018-10-20 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
e7a0c921-3f14-4d5a-a911-be35b3cafb50	2018-10-21 09:00:00+00	2018-10-21 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
479be56f-452a-4b3b-92f7-c1c170abdda8	2018-10-22 09:00:00+00	2018-10-22 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
29dd9a85-4943-40d9-b6d9-58e5a8abe3cc	2018-10-23 09:00:00+00	2018-10-23 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
d3cfe741-e2c4-4826-ba08-ff3bf00fc877	2018-10-25 09:00:00+00	2018-10-25 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
83b67985-7fda-41f5-a08a-feb21f3f0229	2018-10-26 09:00:00+00	2018-10-26 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
b599b016-a2a9-495f-b603-c67cf6dac846	2018-10-27 09:00:00+00	2018-10-27 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
25594bfc-217a-4765-a79e-0fff4002ff86	2018-10-28 09:00:00+00	2018-10-28 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
da55f1d5-ff36-444a-b4d7-cbdb7829ea69	2018-10-29 09:00:00+00	2018-10-29 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
bdb83224-f738-4ea0-8274-2c16d5c1054e	2018-10-30 09:00:00+00	2018-10-30 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
8c002c15-364c-4619-9517-d2a211e6c10f	2018-10-31 09:00:00+00	2018-10-31 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
417e5679-9bff-4864-8045-0c4269c982c4	2018-11-01 09:00:00+00	2018-11-01 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
44658203-a66b-48b2-9a3e-29d4802d6340	2018-11-02 09:00:00+00	2018-11-02 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
880c639c-3297-4951-9263-e986053b2015	2018-11-03 09:00:00+00	2018-11-03 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
908d3de0-df03-431d-b4bf-d7a46d2e0c44	2018-11-04 09:00:00+00	2018-11-04 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
6dccaab8-76e2-4503-9e16-8b2487ca144f	2018-11-05 09:00:00+00	2018-11-05 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
8389fab6-1a2e-4a6c-aa9d-34e45703ec09	2018-11-06 09:00:00+00	2018-11-06 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
08496015-d5f3-4f3d-bad0-f3e8000e8845	2018-11-07 09:00:00+00	2018-11-07 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
444c59ca-0024-4b73-a52f-94264acde68e	2018-11-08 09:00:00+00	2018-11-08 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
701ab601-a952-4273-af91-11bc23c17bdd	2018-11-09 09:00:00+00	2018-11-09 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
4e4de44e-0019-4e71-87e0-9fe611251fdf	2018-11-10 09:00:00+00	2018-11-10 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
a791cc1e-14a9-4677-963e-b6fa0a8aade9	2018-11-11 09:00:00+00	2018-11-11 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
f6af757f-b6a0-40d3-a47c-688c7ccebc52	2018-11-12 09:00:00+00	2018-11-12 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
e18b284e-7168-46b6-9e7c-9ed56516213e	2018-11-13 09:00:00+00	2018-11-13 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
5c76d22c-d6de-4b95-bf16-f3c801cc02b4	2018-11-14 09:00:00+00	2018-11-14 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
20f35e51-ed32-4611-987b-1ace19a5e372	2018-11-15 09:00:00+00	2018-11-15 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
49ae3ba2-221c-479e-b1c8-60379ed2c802	2018-11-16 09:00:00+00	2018-11-16 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
3d55976e-358b-47ca-b82b-e07078f45fa9	2018-11-17 09:00:00+00	2018-11-17 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
495ee342-8cb0-46e2-bd54-4d7557e687c5	2018-11-18 09:00:00+00	2018-11-18 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
d5d4e9cd-09aa-489f-9111-a3ebce63c742	2018-11-19 09:00:00+00	2018-11-19 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
5c994548-f8b9-48d3-9496-9f356890a099	2018-11-20 09:00:00+00	2018-11-20 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
2e796018-71ee-42a8-a741-901b9a54874e	2018-11-21 09:00:00+00	2018-11-21 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
f0bf0af0-4ca0-469d-b13a-3cc4f296d9c7	2018-11-22 09:00:00+00	2018-11-22 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
cf578475-2975-4424-bed4-92b1dc96d583	2018-11-23 09:00:00+00	2018-11-23 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
dbd9ed84-e7b4-4ba1-a2d9-7ae88adfdfe1	2018-11-24 09:00:00+00	2018-11-24 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
01a3e486-5cf4-4f2e-a2cb-38fe1296c804	2018-11-25 09:00:00+00	2018-11-25 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
fc9f9daf-d3a0-4cf5-812f-c0cae7200fcc	2018-11-26 09:00:00+00	2018-11-26 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
0c89d72b-9e7d-4522-bd51-4856a0e836f8	2018-11-27 09:00:00+00	2018-11-27 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	f
8e6c7ee1-5668-4fd3-a8cc-7dfe7d141d35	2018-10-18 09:00:00+00	2018-10-18 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	t
ca66ea13-74d5-486a-8a33-985dc98dd0c3	2018-10-24 09:00:00+00	2018-10-24 17:00:00+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	9a67cb3a-debc-4c7a-ba45-5bb073db776f	t
\.


--
-- Data for Name: tasks_assessmenttasktemplate; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_assessmenttasktemplate (id, start_on_day, frequency, repeat_amount, appear_time, due_time, tracks_outcome, tracks_satisfaction, plan_template_id, name) FROM stdin;
9a67cb3a-debc-4c7a-ba45-5bb073db776f	0	daily	-1	09:00:00	17:00:00	t	f	719563fb-6394-47b8-89e0-3f6f4fad9c9f	Depression Assessment
\.


--
-- Data for Name: tasks_medicationtask; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_medicationtask (id, appear_datetime, due_datetime, status, medication_task_template_id) FROM stdin;
20262ae6-f4ea-4077-9812-fc0cebb2ab0f	2018-10-10 09:00:00.565467+00	2018-10-10 17:00:00.565439+00	undefined	e636f748-9511-4537-9014-64e93b7dca78
b6a52d0d-df9e-4cda-a0d7-9607ab3e7fbf	2018-10-16 09:00:00+00	2018-10-16 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
96d4a42a-5b20-4b2d-86da-43580443c52f	2018-10-17 09:00:00+00	2018-10-17 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
5df96e94-c761-455b-81a4-0ed4511eb5b6	2018-10-18 09:00:00+00	2018-10-18 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
382fcdd4-954f-4433-9245-2ef89b7c175f	2018-10-19 09:00:00+00	2018-10-19 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
f4f240fb-aa01-419a-a6ab-9ecab0b54ed8	2018-10-20 09:00:00+00	2018-10-20 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
d03f1fb3-bdc4-45ff-b3a2-c562a472a802	2018-10-21 09:00:00+00	2018-10-21 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
17dc3220-effc-4ab5-8e21-2cff0c99296a	2018-10-22 09:00:00+00	2018-10-22 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
163414a0-a62b-4ab6-ba85-46aa37306c7c	2018-10-23 09:00:00+00	2018-10-23 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
654b3ea0-1b87-46a3-93ef-ef7f743d90dc	2018-10-25 09:00:00+00	2018-10-25 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
2247a342-e6c0-40e7-b8d6-bbebe481cfce	2018-10-26 09:00:00+00	2018-10-26 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
fc49c4ff-77ff-4216-ad93-b2786acf9858	2018-10-27 09:00:00+00	2018-10-27 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
a7c8b09c-ec02-4bcc-878f-0afc0d3ed3c4	2018-10-28 09:00:00+00	2018-10-28 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
7d9c5c1a-95e6-4866-8077-318a5c8a3a8d	2018-10-29 09:00:00+00	2018-10-29 17:00:00+00	undefined	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
cbce8e24-9324-475d-9c8a-877fe08459ad	2018-10-17 09:00:00+00	2018-10-17 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
655667ce-520a-416b-882b-1488611be91b	2018-10-18 09:00:00+00	2018-10-18 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
a4a1ad8e-43cf-47bd-ab13-03dceb42b270	2018-10-19 09:00:00+00	2018-10-19 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
c01e1130-27c2-4fa9-bfcb-914e3170cc79	2018-10-20 09:00:00+00	2018-10-20 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
293ffa7c-c31b-4810-8146-c7b82174c761	2018-10-21 09:00:00+00	2018-10-21 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
c6733352-3b4c-4cb9-8779-d5ab6a400430	2018-10-22 09:00:00+00	2018-10-22 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
e968fa5c-27bd-4bef-ab1d-a7802620ef50	2018-10-23 09:00:00+00	2018-10-23 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
72426138-5666-4293-b956-6150b0032eda	2018-10-24 09:00:00+00	2018-10-24 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
0056f95f-59b4-40a5-af0c-4fd34c9db006	2018-10-25 09:00:00+00	2018-10-25 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
e03ddb09-d59c-4a41-8cba-992b096948bd	2018-10-26 09:00:00+00	2018-10-26 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
18d3bae7-0953-44ba-b75e-f5a323b703db	2018-10-27 09:00:00+00	2018-10-27 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
3d05a389-9367-417b-b64a-92d25bbb8350	2018-10-28 09:00:00+00	2018-10-28 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
2c1b807b-eb69-4888-b15e-a62a49e3a72c	2018-10-29 09:00:00+00	2018-10-29 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
a1005526-6f0f-465d-8e3c-dad48fe1eaa0	2018-10-30 09:00:00+00	2018-10-30 17:00:00+00	undefined	b4ecef1d-8fd6-4e17-b64a-6a329cf15256
fc062bf8-59eb-4906-8774-c64eeaf28fdc	2018-10-24 09:00:00+00	2018-10-24 17:00:00+00	done	cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb
\.


--
-- Data for Name: tasks_medicationtasktemplate; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_medicationtasktemplate (id, start_on_day, frequency, repeat_amount, appear_time, due_time, patient_medication_id, plan_id) FROM stdin;
e636f748-9511-4537-9014-64e93b7dca78	0	once	-1	09:00:00	17:00:00	6e992289-11a6-40e7-806b-1815d71e67f6	fdb25787-150f-4117-a757-b1cd399b98f3
cc8cbb6b-82fe-4fd1-aa20-c244a3884cdb	0	daily	14	09:00:00	17:00:00	6e992289-11a6-40e7-806b-1815d71e67f6	fdb25787-150f-4117-a757-b1cd399b98f3
b4ecef1d-8fd6-4e17-b64a-6a329cf15256	0	daily	14	09:00:00	17:00:00	c72d3ad9-e3a5-4d42-adf2-1a8a229b4546	c222e159-26f4-4bd6-9ea5-863f0cb0df71
\.


--
-- Data for Name: tasks_patienttask; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_patienttask (id, appear_datetime, due_datetime, status, patient_task_template_id, plan_id) FROM stdin;
433c0606-1675-4a85-b0ec-27bf975d1081	2018-10-05 16:00:00+00	2018-10-05 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
ea1fddea-26e4-41ff-bf28-159dfc7f4aec	2018-10-06 16:00:00+00	2018-10-06 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
b23c2de6-a785-4cd6-8abc-c7d880938312	2018-10-07 16:00:00+00	2018-10-07 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
468024f2-a122-48f1-9021-22ebf97f544e	2018-10-08 16:00:00+00	2018-10-08 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
3f8f880e-eb53-49fd-b7b4-d2e9a940ba3e	2018-10-09 16:00:00+00	2018-10-09 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
74c8b35c-92a7-4dac-b8b1-926da18e252f	2018-10-10 16:00:00+00	2018-10-10 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
1918920c-5cce-423c-be26-985c94f3b9e2	2018-10-11 16:00:00+00	2018-10-11 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
9f066ccc-a0b4-44cf-9a5f-28f98a36b17a	2018-10-12 16:00:00+00	2018-10-12 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
34a594a7-e8eb-489d-b0a2-e79a4892eeca	2018-10-13 16:00:00+00	2018-10-13 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
f5f32dfe-7258-4533-a65c-e9a63a085adc	2018-10-14 16:00:00+00	2018-10-14 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
f283b652-1b4a-428c-93ac-da9cbee0f32f	2018-10-15 16:00:00+00	2018-10-15 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
22bdc7ae-85c0-4f12-9efa-d67ec5f5e09f	2018-10-17 16:00:00+00	2018-10-17 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
33f50df7-4fb5-484a-840d-99bd1a154d19	2018-10-18 16:00:00+00	2018-10-18 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
50d6a55f-3cbf-4525-9990-f59d30e281c6	2018-10-19 16:00:00+00	2018-10-19 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
eddcc1f8-5367-46b4-b4eb-1251c48a585c	2018-10-20 16:00:00+00	2018-10-20 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
839348b7-c6f6-494d-be8e-6120da2b3016	2018-10-21 16:00:00+00	2018-10-21 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
6da744dc-0c27-43eb-99d3-374286510785	2018-10-22 16:00:00+00	2018-10-22 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
f2937846-5527-4526-9978-e328036f3ba2	2018-10-24 16:00:00+00	2018-10-24 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
4a1c70a6-0de7-4b20-b9e4-17aa83f4ac08	2018-10-25 16:00:00+00	2018-10-25 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
5f03cfec-4abd-42cf-bacd-b774e7d4ed37	2018-10-26 16:00:00+00	2018-10-26 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
a7624a78-0bb6-4469-9973-16a756a85069	2018-10-27 16:00:00+00	2018-10-27 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
50134072-6efc-4187-b437-558311a49c34	2018-10-29 16:00:00+00	2018-10-29 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
7973c983-c6fd-4db8-9fa3-e0c7f02343ba	2018-10-30 16:00:00+00	2018-10-30 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
2db2b8b1-1699-43cf-b32d-90020288dcbf	2018-10-31 16:00:00+00	2018-10-31 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
8e1e96bf-5f38-45c9-8552-fd22f93d2a20	2018-11-01 16:00:00+00	2018-11-01 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
3df0de3a-3d2f-45c8-a695-067c3661d170	2018-11-02 16:00:00+00	2018-11-02 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
d7b01237-b60f-4537-ac19-94363ff0c00b	2018-11-03 16:00:00+00	2018-11-03 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
edc779f5-0668-4c9e-b649-ba5e5da7f4a9	2018-11-04 16:00:00+00	2018-11-04 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
7201d515-0acf-47a6-b313-77d4ea9db7f0	2018-11-05 16:00:00+00	2018-11-05 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
d9ef3930-481c-4ad8-9234-523b81bae534	2018-11-06 16:00:00+00	2018-11-06 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
bb977912-e301-497e-86a7-ec19d54bb671	2018-11-07 16:00:00+00	2018-11-07 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
8f8455fc-c7aa-4124-a4a4-58376fa142bd	2018-11-08 16:00:00+00	2018-11-08 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
ccdc6d5b-91f4-4bd2-84c9-d59153fab0a6	2018-11-09 16:00:00+00	2018-11-09 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
ae3a01e9-0d5f-41f3-9b4d-950965e25b27	2018-11-10 16:00:00+00	2018-11-10 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
155f328d-3ebe-4b18-8387-562787f02319	2018-11-11 16:00:00+00	2018-11-11 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
33cc75f2-346f-4096-a5b9-10904a483932	2018-11-12 16:00:00+00	2018-11-12 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
5b939ea4-cb55-47f2-aa0c-101d971c8970	2018-11-13 16:00:00+00	2018-11-13 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
033fc223-42ef-4c73-b63d-e810336cb9bb	2018-11-14 16:00:00+00	2018-11-14 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
5be2e013-538a-4edd-b368-6f8b2b35f6d9	2018-11-15 16:00:00+00	2018-11-15 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
b2d61428-932e-4ff5-ae21-dbc4c3eba92d	2018-11-16 16:00:00+00	2018-11-16 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
c470f38b-5552-4792-a184-b4a444c2617c	2018-10-05 11:00:00+00	2018-10-05 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
9882c850-db0a-46b7-9826-5713479bb1c9	2018-10-06 11:00:00+00	2018-10-06 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
29a3bffd-4ecf-46db-b233-1da6f46aea10	2018-10-07 11:00:00+00	2018-10-07 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
b8bf6d5a-06b4-4f59-b1a3-954cd5fc839f	2018-10-08 11:00:00+00	2018-10-08 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
7d3caae3-cb77-4e29-9bc8-b4e570c69845	2018-10-09 11:00:00+00	2018-10-09 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
4d4ffcf6-8c1f-4cc1-aab4-eb792acbf947	2018-10-10 11:00:00+00	2018-10-10 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
6d45d8fe-ad51-4ff5-8096-7016e4764138	2018-10-11 11:00:00+00	2018-10-11 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
4bffb6eb-2aa6-44b4-9bca-aed3287df73d	2018-10-12 11:00:00+00	2018-10-12 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
245abeba-df96-4082-a2ad-64915747bcc2	2018-10-13 11:00:00+00	2018-10-13 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
c77da6c6-3f82-4aaf-9e0b-4a968e94a1c4	2018-10-14 11:00:00+00	2018-10-14 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
a93d7717-bf04-486e-88ce-11e56bf78d8d	2018-10-15 11:00:00+00	2018-10-15 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
cb5009ec-2215-4e75-bba4-93585b7972b7	2018-10-17 11:00:00+00	2018-10-17 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
ddea11fb-09db-4e4c-b896-2dd257bcb954	2018-10-18 11:00:00+00	2018-10-18 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
43171073-ce34-4bd3-a7f4-093df328d0b4	2018-10-19 11:00:00+00	2018-10-19 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
2794ce63-85dd-4673-8f7f-a90b0e6e6005	2018-10-20 11:00:00+00	2018-10-20 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
5b27ffc5-b3da-4bda-b360-0ed4029c0f65	2018-10-21 11:00:00+00	2018-10-21 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
0349a0a5-1346-45a9-bd01-d457d826117c	2018-10-22 11:00:00+00	2018-10-22 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
4cba541b-7752-43c0-84a6-401e2df8b12a	2018-10-25 11:00:00+00	2018-10-25 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
e965fd6b-7a81-471d-90d7-e6e1f3f75779	2018-10-26 11:00:00+00	2018-10-26 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
546e0e86-3a81-4128-a3e1-ebb68f9909e1	2018-10-27 11:00:00+00	2018-10-27 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
ecc8966d-330f-43f1-83d9-363b4c1d3856	2018-10-28 11:00:00+00	2018-10-28 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
fa48ac39-5da8-46f2-84f0-b5d64cfdaf82	2018-10-29 11:00:00+00	2018-10-29 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
7b49cff7-0692-46aa-8c66-97d221e48a84	2018-10-30 11:00:00+00	2018-10-30 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
2b3fa35b-8658-453b-bd2a-333fa45ce487	2018-10-31 11:00:00+00	2018-10-31 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
1756cf8e-74c1-4322-be5c-e2a221d3ebc9	2018-11-02 11:00:00+00	2018-11-02 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
b3cf1e7e-8971-44ba-90a6-5692193291ce	2018-11-03 11:00:00+00	2018-11-03 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
000b8a57-53d6-4230-afde-d2fe7ab788e0	2018-11-04 11:00:00+00	2018-11-04 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
7d5266ad-55bb-456d-b4c2-ea477e2acede	2018-11-05 11:00:00+00	2018-11-05 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
cd58c6fe-dcc2-42eb-92bb-3d53ae0f04cc	2018-10-16 16:00:00+00	2018-10-16 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
876ea202-544a-489d-a7fa-d7489330789b	2018-10-23 16:00:00+00	2018-10-23 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
31ea2e5c-12a9-4750-95e6-97c5d3960a08	2018-10-16 16:00:00+00	2018-10-16 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
1f5cb4f6-7ea5-4600-b747-bfedde3b0a90	2018-10-24 11:00:00+00	2018-10-24 02:00:00+00	done	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
bdd11f62-4b81-461b-9e2f-647ce6bfe07a	2018-10-28 16:00:00+00	2018-10-28 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	fdb25787-150f-4117-a757-b1cd399b98f3
2b2dbfc9-6038-41ee-96e6-c13e739cc8f8	2018-11-01 11:00:00+00	2018-11-01 02:00:00+00	done	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
3801bee9-c22f-4c15-91db-4c7f8d659f7e	2018-11-06 11:00:00+00	2018-11-06 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
a1732875-04e7-4a22-acb1-943c7e0196d3	2018-11-07 11:00:00+00	2018-11-07 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
318a49de-f8a0-46b0-a8e8-59afefa938b7	2018-11-08 11:00:00+00	2018-11-08 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
d24d4645-8c09-4a28-8df2-53a1e28780d8	2018-11-09 11:00:00+00	2018-11-09 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
38e554e8-5196-4ddb-8a34-abd9ff5e5cb1	2018-11-10 11:00:00+00	2018-11-10 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
cb267a77-2b70-48c1-a2af-275cea0b564d	2018-11-11 11:00:00+00	2018-11-11 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
d3ba3451-11be-455e-bbda-e20044b7f84d	2018-11-12 11:00:00+00	2018-11-12 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
244123ff-2c28-4f8c-aed6-89514faad60e	2018-11-13 11:00:00+00	2018-11-13 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
e9abdf8c-563a-43bc-b167-a871c7de9c16	2018-11-14 11:00:00+00	2018-11-14 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
b82674e7-bfbb-4b94-ba88-44f11592c9aa	2018-11-15 11:00:00+00	2018-11-15 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
3f7aa24d-9d79-4a04-a51a-4cc59d72ec0b	2018-11-16 11:00:00+00	2018-11-16 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
c7d051a3-5bc2-4888-98fb-fd03d7b1500d	2018-10-05 06:00:00+00	2018-10-05 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
fa0b3e78-724b-4958-a933-caca265d9d36	2018-10-06 06:00:00+00	2018-10-06 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
d38edf26-210d-48ac-ad39-ebf96ccdd353	2018-10-07 06:00:00+00	2018-10-07 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
40e20ed0-0ee3-477c-9708-afaec9a458ba	2018-10-08 06:00:00+00	2018-10-08 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
8682e26e-bb86-489a-92b5-3f79bf12255d	2018-10-09 06:00:00+00	2018-10-09 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
555990a0-a44a-4911-a810-7c7b1f0df758	2018-10-10 06:00:00+00	2018-10-10 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
36a6d259-7671-4634-bc7a-c40d9d389b09	2018-10-11 06:00:00+00	2018-10-11 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
ddacd9a3-7aa7-4824-a4f9-ca77c1cc6fde	2018-10-12 06:00:00+00	2018-10-12 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
96285c9b-004a-4e9a-b3b3-82a9d28ce074	2018-10-13 06:00:00+00	2018-10-13 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
e9080322-f704-4889-8628-e52907c55546	2018-10-14 06:00:00+00	2018-10-14 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
e83905fc-bac6-48ef-a1ed-966b72748c9f	2018-10-15 06:00:00+00	2018-10-15 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
ec30bb39-4658-47cb-a464-308a531de962	2018-10-17 06:00:00+00	2018-10-17 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
60efc80b-ff1a-4dc7-bc46-0f500f5931e3	2018-10-18 06:00:00+00	2018-10-18 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
0d1d241b-a92d-4557-b82d-b51a88e7bc97	2018-10-19 06:00:00+00	2018-10-19 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
f46b7822-c319-4c7e-9e55-aad83a4956b8	2018-10-20 06:00:00+00	2018-10-20 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
68d372f4-198e-4556-acd3-c09383e1ffa8	2018-10-21 06:00:00+00	2018-10-21 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
607e5b5d-3625-44bb-bf7f-8aa7b5d9b16c	2018-10-22 06:00:00+00	2018-10-22 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
043bd2c3-1a49-43be-b96b-4e1300582f34	2018-10-24 06:00:00+00	2018-10-24 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
8e7b59d0-c324-4ddc-8df3-947b3626049e	2018-10-25 06:00:00+00	2018-10-25 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
e08590a0-c022-4bca-bb9c-8fc5ee91aa26	2018-10-26 06:00:00+00	2018-10-26 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
67b0322e-2179-4401-9406-0bb2ebeb32de	2018-10-27 06:00:00+00	2018-10-27 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
3fee688a-ffed-46a1-9112-42a7658a60a0	2018-10-28 06:00:00+00	2018-10-28 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
8bc837f2-b9ac-4dab-bc01-4c1bfea5e6ef	2018-10-29 06:00:00+00	2018-10-29 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
48b846d0-0cd1-438d-9afa-0bc0e0e0d07e	2018-10-30 06:00:00+00	2018-10-30 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
50c5d06c-63a1-4e42-acf2-521194de2fa5	2018-10-31 06:00:00+00	2018-10-31 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
e09d1bff-4557-4c9b-93c0-1b43813c9604	2018-11-02 06:00:00+00	2018-11-02 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
a2518de5-2534-4b5b-9594-7fcfe7d21130	2018-11-03 06:00:00+00	2018-11-03 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
bbb9fcba-d0fb-4bb5-95bb-d1401b580a42	2018-11-04 06:00:00+00	2018-11-04 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
c93bb48a-a887-42a9-a98e-87f409b53152	2018-11-05 06:00:00+00	2018-11-05 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
55e59752-c488-44f0-9121-149f7dce0f92	2018-11-06 06:00:00+00	2018-11-06 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
d223a7e5-0863-43e9-bb1b-84aff6691fec	2018-11-07 06:00:00+00	2018-11-07 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
9bed539f-6e40-4c37-be35-7dc54a92a1e8	2018-11-08 06:00:00+00	2018-11-08 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
f9c06b20-33e7-4982-a777-540a6ee310ad	2018-11-09 06:00:00+00	2018-11-09 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
90517c86-3c49-4c95-aa32-d3f588b6097b	2018-11-10 06:00:00+00	2018-11-10 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
624a5a11-5745-4c46-b3a7-9a40394160e6	2018-11-11 06:00:00+00	2018-11-11 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
b6d71b12-1a18-4e50-9052-bf7f798f113e	2018-11-12 06:00:00+00	2018-11-12 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
f51c2864-eb64-4bba-af21-fccee81cb4cb	2018-11-13 06:00:00+00	2018-11-13 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
d433e8c3-09be-471b-a851-81367a5b1d15	2018-11-14 06:00:00+00	2018-11-14 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
1875eed9-450a-4b13-96f9-73e8ccfdf7ca	2018-11-15 06:00:00+00	2018-11-15 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
f51df6b0-39dc-42ec-bec2-9c866aceaca4	2018-11-16 06:00:00+00	2018-11-16 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
5b8e7552-7277-4607-9027-09a511fde7ff	2018-10-05 09:00:00+00	2018-10-05 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
15f133f5-8c6c-463c-9fe2-995aa433cefb	2018-10-07 09:00:00+00	2018-10-07 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
e33fed1b-3408-4ad0-a0a5-08422a56a930	2018-10-09 09:00:00+00	2018-10-09 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
522f20c7-0852-4aba-82dd-134dccf0e138	2018-10-11 09:00:00+00	2018-10-11 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
ce5c5017-daa1-4d69-83ff-7acc9543c25f	2018-10-13 09:00:00+00	2018-10-13 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
b437f18d-f02c-4f09-8468-8aa2b1932eea	2018-10-15 09:00:00+00	2018-10-15 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
f0dccc81-2cea-4da6-8054-5a80da0d4332	2018-10-17 09:00:00+00	2018-10-17 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
80d79330-961a-48ba-a0e9-089b2ba045d3	2018-10-19 09:00:00+00	2018-10-19 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
65a2cb15-4e8d-437f-aab9-dc376c6afabf	2018-10-21 09:00:00+00	2018-10-21 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
0aac6a22-ca7a-413b-95d8-2862f7e2adb6	2018-10-25 09:00:00+00	2018-10-25 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
d4814826-e2c7-42df-8eba-599c6a3d0127	2018-10-27 09:00:00+00	2018-10-27 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
c7f992b5-78c9-4174-a377-1617b0dc7acf	2018-10-29 09:00:00+00	2018-10-29 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
435b70d2-f248-4c0c-8b50-f942164d6518	2018-10-31 09:00:00+00	2018-10-31 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
01a02c17-8802-4166-aa6f-1a66b319ca35	2018-11-02 09:00:00+00	2018-11-02 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
b086c3ef-1c18-475a-ad8b-780eb9ac730d	2018-11-04 09:00:00+00	2018-11-04 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
f86f6724-5a73-4d48-b196-5e1c2376570f	2018-11-06 09:00:00+00	2018-11-06 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
33e80c88-04f0-401e-8655-f2e9ee55c238	2018-11-08 09:00:00+00	2018-11-08 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
1f28e3db-7e53-49b9-ad40-80e34079b169	2018-11-10 09:00:00+00	2018-11-10 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
4ead459d-3745-4bcc-aee4-d035ac3ec8f6	2018-11-12 09:00:00+00	2018-11-12 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
95247b52-bbc5-4f6d-9342-a7945cc7d701	2018-11-14 09:00:00+00	2018-11-14 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
d2bedf0b-6da7-408b-b627-f0dd0a8ee869	2018-10-23 06:00:00+00	2018-10-23 10:00:00+00	done	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
56aa5b41-a571-4cb1-bc5e-0ccf98b1ed3b	2018-10-17 16:00:00+00	2018-10-17 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
98358960-0ed6-4150-bf30-67feb9d63ede	2018-11-01 06:00:00+00	2018-11-01 10:00:00+00	done	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
a1a519e3-99d1-420d-ac73-709aab0293cf	2018-11-16 09:00:00+00	2018-11-16 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
e64fae06-481b-4e3f-a7d9-570d59507c4e	2018-10-25 16:00:00+00	2018-10-25 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
158ecb4e-80db-49ac-a3f4-9a0c743506d8	2018-10-26 16:00:00+00	2018-10-26 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
2e235555-e4f3-48e9-b328-3ac65d1d7693	2018-10-27 16:00:00+00	2018-10-27 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
be1afda1-9c14-4741-8b16-018514636a98	2018-10-28 16:00:00+00	2018-10-28 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
131f0935-60c8-451c-88ee-f5ba98456130	2018-10-29 16:00:00+00	2018-10-29 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
6d89fa2f-4d16-4d17-8f6f-d040dd6d1d94	2018-10-30 16:00:00+00	2018-10-30 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
c510d7da-9c72-48b1-afbe-228f0634a31b	2018-10-31 16:00:00+00	2018-10-31 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
c13594e4-1054-4485-b1af-1e35863dc1d9	2018-11-01 16:00:00+00	2018-11-01 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
167cddf7-0044-4f2b-914b-a1b8f87ce97d	2018-11-02 16:00:00+00	2018-11-02 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
66589ab5-5a10-458e-b1e4-a8278a062d56	2018-11-03 16:00:00+00	2018-11-03 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
136974a8-914d-41e9-92f3-7fae28454a18	2018-11-04 16:00:00+00	2018-11-04 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
8204f28b-1882-4c2d-b50c-42e2c2f0f63e	2018-11-05 16:00:00+00	2018-11-05 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
f3148742-cce8-4d8d-982c-f70b65d37b2b	2018-11-06 16:00:00+00	2018-11-06 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
501ef00a-38e2-4ef2-86b0-54840046e326	2018-11-07 16:00:00+00	2018-11-07 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
a6a4d5fc-cff4-4e54-a3f1-687641fb946b	2018-11-08 16:00:00+00	2018-11-08 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
387f5dab-1a56-476f-9b66-1d70a6df2a78	2018-11-09 16:00:00+00	2018-11-09 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
73ff54e1-52da-4f1a-8e41-57ca2805fb82	2018-11-10 16:00:00+00	2018-11-10 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
941ee9b7-f964-4cac-bc4a-82fdafaf4f8e	2018-11-11 16:00:00+00	2018-11-11 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
24896d91-08a1-425c-aa4c-7bb105e7b33a	2018-11-12 16:00:00+00	2018-11-12 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
1f6a82d7-1573-4e56-ab36-37f723e2a103	2018-11-13 16:00:00+00	2018-11-13 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
48bbecf1-7273-44c9-81d3-efae4664c29b	2018-11-14 16:00:00+00	2018-11-14 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
5121944d-4c15-4fe4-8bfb-6e75df160235	2018-11-15 16:00:00+00	2018-11-15 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
c069ed9a-4cca-4a15-818d-d53a7176ff15	2018-11-16 16:00:00+00	2018-11-16 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
f10803b3-1771-49bb-bd1f-3495802cb234	2018-11-17 16:00:00+00	2018-11-17 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
9ee28b9e-b3c0-4992-a936-a5a9274980ca	2018-11-18 16:00:00+00	2018-11-18 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
8129650f-03ea-4584-b125-ee05918a0215	2018-11-19 16:00:00+00	2018-11-19 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
b6170a14-b30a-4473-9c54-b2d668ecfb31	2018-11-20 16:00:00+00	2018-11-20 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
b3ca09e7-183c-48ca-bd7c-f78396717c22	2018-11-21 16:00:00+00	2018-11-21 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
fdd9e31a-6136-4bc8-be1b-ce9de967e3ab	2018-11-22 16:00:00+00	2018-11-22 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
4adea31e-a0c4-44dc-afcd-9e9c6162a80e	2018-11-23 16:00:00+00	2018-11-23 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
6e899c52-f86a-4c7e-b5e9-848ba73748bc	2018-11-24 16:00:00+00	2018-11-24 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
c260a1ee-b61c-486c-a63a-2ff2e1deaf9e	2018-11-25 16:00:00+00	2018-11-25 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
b7941e00-f11e-46d2-96d3-a10bc519a4de	2018-11-26 16:00:00+00	2018-11-26 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
882299b2-c484-4ae1-bc77-80c4c9ec57d3	2018-11-27 16:00:00+00	2018-11-27 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
b6e7caea-a3ab-41de-b754-94728dd1e04b	2018-10-20 11:00:00+00	2018-10-20 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
c9a33db9-d245-4c83-9c09-c310bef55110	2018-10-21 11:00:00+00	2018-10-21 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
364128e6-4b2e-4acc-a3b2-39eebecbb6b2	2018-10-22 11:00:00+00	2018-10-22 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
264933b7-e5b0-4d5e-93b2-c31fcc89820c	2018-10-23 11:00:00+00	2018-10-23 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
b40084f5-e142-4390-bcd3-0a0f1f428f34	2018-10-26 11:00:00+00	2018-10-26 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
9e9ec561-ec76-4c6f-8566-c3ea549e2f1a	2018-10-27 11:00:00+00	2018-10-27 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
52419c3d-22d4-46eb-9876-fb6c2a8796fe	2018-10-28 11:00:00+00	2018-10-28 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
7f5efd93-7ac4-4a0e-b626-da3c86a475f8	2018-10-29 11:00:00+00	2018-10-29 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
ff987fb0-a65b-4fc3-9c10-1473a5ecae34	2018-10-30 11:00:00+00	2018-10-30 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
c50b21ab-0a62-4936-b62d-63c1be90eaf4	2018-10-31 11:00:00+00	2018-10-31 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
a06873a0-ff91-462a-a4e5-cc58fab245d0	2018-11-01 11:00:00+00	2018-11-01 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
78b7e81c-3354-4fcc-9acd-5fd69c4d5275	2018-11-02 11:00:00+00	2018-11-02 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
5ca899aa-6fc9-4f0a-833d-661b6d2e0d21	2018-11-03 11:00:00+00	2018-11-03 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
522f0fdd-de47-4220-902e-7f1d6689f1af	2018-11-04 11:00:00+00	2018-11-04 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
30745bc9-647c-4648-a8d0-df080b4e17c3	2018-11-05 11:00:00+00	2018-11-05 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
a7c8c331-3c49-4ba2-a509-7dad52171a3c	2018-11-06 11:00:00+00	2018-11-06 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
3857fbe7-f726-42f8-bb47-0959373dfa7e	2018-11-07 11:00:00+00	2018-11-07 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
85b0d1ae-cb97-4bb6-85da-0a7f4ae64a50	2018-11-08 11:00:00+00	2018-11-08 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
c2e35f24-1f05-4a05-8f19-4b3f1900fdfe	2018-11-09 11:00:00+00	2018-11-09 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
5783437e-dd40-432d-a0c2-23fafe0829ce	2018-11-10 11:00:00+00	2018-11-10 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
9e7cd6ae-20f7-46a6-aa2d-7e3802571862	2018-11-11 11:00:00+00	2018-11-11 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
ae87f10a-8905-4be1-abdb-4c768a8321c0	2018-11-12 11:00:00+00	2018-11-12 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
ea458b51-f718-4a12-9f10-59ef14f7e737	2018-11-13 11:00:00+00	2018-11-13 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
4025757b-f218-41c1-a943-74b5169f9ac4	2018-11-14 11:00:00+00	2018-11-14 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
09d8eeb6-3d56-4d89-aec2-d7783c201315	2018-11-15 11:00:00+00	2018-11-15 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
580132bd-cdc3-4eab-9573-09a5e62ec0f7	2018-11-16 11:00:00+00	2018-11-16 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
89294205-01f9-4853-be0f-44d13a3f98db	2018-11-17 11:00:00+00	2018-11-17 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
6a4c7537-32a7-4591-a8ee-87c2b66043d7	2018-10-23 16:00:00+00	2018-10-23 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
d6088b84-69da-44aa-a2c4-8d23ba7cb62b	2018-10-22 16:00:00+00	2018-10-22 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
02713cf0-67aa-4076-840e-57f824b9bca4	2018-10-21 16:00:00+00	2018-10-21 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
c3c814bb-c992-4d8f-8fff-0a015e8d5a63	2018-10-20 16:00:00+00	2018-10-20 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
0d3e738b-bd42-4581-8516-16532c8142ca	2018-10-19 16:00:00+00	2018-10-19 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
c5e85c44-557a-4d48-b095-60cf73d7e72b	2018-10-18 16:00:00+00	2018-10-18 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
b59cda4f-82a3-40f0-b89b-ca6710b39088	2018-10-16 11:00:00+00	2018-10-16 02:00:00+00	done	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
485d023a-d51f-40f2-9975-af3abc06f1a4	2018-10-17 11:00:00+00	2018-10-17 02:00:00+00	done	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
0529e786-d9b4-4917-9fc5-996e41bb24e1	2018-10-18 11:00:00+00	2018-10-18 02:00:00+00	done	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
0478bc32-17ad-4ed3-8dba-6c16a9a74005	2018-10-19 11:00:00+00	2018-10-19 02:00:00+00	done	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
d0ef3d9e-bf4b-47dc-b9e7-d9859ab9f710	2018-10-25 11:00:00+00	2018-10-25 02:00:00+00	done	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
6d3db8cc-2fcd-4326-8f4a-43db1a24efef	2018-10-24 11:00:00+00	2018-10-24 02:00:00+00	done	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
86ee9b1a-071e-4bb4-9d15-7ed93eac5bde	2018-11-18 11:00:00+00	2018-11-18 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
80e151a1-5046-4247-81a5-62c1496edf52	2018-11-19 11:00:00+00	2018-11-19 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
5a75c0f6-87ff-4466-8a65-e0dc8f04c325	2018-11-20 11:00:00+00	2018-11-20 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
1fcf1914-1a4a-4023-8372-df3f78047140	2018-11-21 11:00:00+00	2018-11-21 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
e991cdb5-77d6-4934-a351-1da14fc19fbe	2018-11-22 11:00:00+00	2018-11-22 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
9c272897-c928-4587-b2ee-3e443e19e116	2018-11-23 11:00:00+00	2018-11-23 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
945ccfec-5d3b-4062-b687-bef40b63273e	2018-11-24 11:00:00+00	2018-11-24 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
999cd8d1-6d3a-4ea0-aa86-4ab112bf13ae	2018-11-25 11:00:00+00	2018-11-25 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
ad2f515b-0299-478a-963c-f618ce8aa2dd	2018-11-26 11:00:00+00	2018-11-26 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
b976d52b-369c-4f86-b907-660cc97c94f2	2018-11-27 11:00:00+00	2018-11-27 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	a52bdf43-4e23-4d89-a931-cb36e6979a12
77d4dd1a-ae66-48df-9c47-e72e38b5f03d	2018-10-16 06:00:00+00	2018-10-16 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
2c1253a8-b270-4b05-bdbc-30b6745b1cdb	2018-10-17 06:00:00+00	2018-10-17 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
6af4a630-e090-49bc-ad3e-cd41f039f03b	2018-10-18 06:00:00+00	2018-10-18 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
9fe19a86-0a20-476a-8e39-e13df0e841a9	2018-10-19 06:00:00+00	2018-10-19 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
bf5cc956-0fc6-4c56-847d-82f08f4e63b8	2018-10-20 06:00:00+00	2018-10-20 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
67850b1b-e38f-4712-901d-236c8f6e825a	2018-10-21 06:00:00+00	2018-10-21 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
ea841ce9-b7cd-47b3-9946-5cef71217cda	2018-10-22 06:00:00+00	2018-10-22 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
898b52ed-6d6b-4eb3-a09c-6364a35cf410	2018-10-23 06:00:00+00	2018-10-23 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
178703db-3913-4870-8ff6-91411e0d35ce	2018-10-25 06:00:00+00	2018-10-25 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
7b32414b-2224-4b38-b33f-13565359b582	2018-10-26 06:00:00+00	2018-10-26 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
d47faf95-2dd2-4637-a4f8-7efb6ff26fca	2018-10-27 06:00:00+00	2018-10-27 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
44b0ac02-97ce-4bcf-8fb6-9e5a3bed5ed4	2018-10-28 06:00:00+00	2018-10-28 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
f6fc0bd2-16e1-4bd0-af96-dfd1bc6901fb	2018-10-29 06:00:00+00	2018-10-29 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
f50e6527-2703-42ac-8eb8-6516ab581887	2018-10-30 06:00:00+00	2018-10-30 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
72fc0fbd-aabb-4fa7-9937-ff3d311f7d5c	2018-10-31 06:00:00+00	2018-10-31 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
fa9d4ccc-d937-4d40-8fb8-93eeee1adf23	2018-11-01 06:00:00+00	2018-11-01 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
914ca716-20c1-419e-8c38-da3fe76b18f3	2018-11-02 06:00:00+00	2018-11-02 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
813c3397-8c1e-4177-b2d8-6c1bf8eacaa5	2018-11-03 06:00:00+00	2018-11-03 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
bfa91059-c59b-42bd-9945-55d89fb07b46	2018-11-04 06:00:00+00	2018-11-04 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
8426f70e-98ec-4651-93c2-a338e298d849	2018-11-05 06:00:00+00	2018-11-05 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
a4f056a9-ec82-4686-a6ec-6ef6b97c53f4	2018-11-06 06:00:00+00	2018-11-06 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
81d6bd96-19fa-4a71-8081-d0d6d54e54d5	2018-11-07 06:00:00+00	2018-11-07 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
39bd8eee-bb9a-4c21-95ab-2f050a94e7d1	2018-11-08 06:00:00+00	2018-11-08 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
b0e97860-d623-4ddb-b877-bdeaba5fe5b0	2018-11-09 06:00:00+00	2018-11-09 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
51617f8c-bfbc-486b-a258-019c50533da5	2018-11-10 06:00:00+00	2018-11-10 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
f6a0f2b9-eaa2-4dfc-ba72-b0b35c81f920	2018-11-11 06:00:00+00	2018-11-11 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
0e0b7398-7ad2-4e44-acce-77d87f0acfd5	2018-11-12 06:00:00+00	2018-11-12 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
96e51b06-22fa-47aa-ab90-3541930d3a4b	2018-11-13 06:00:00+00	2018-11-13 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
ddd5e0cd-3897-4a75-8983-76b7f3056d91	2018-11-14 06:00:00+00	2018-11-14 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
a118ca89-c3e7-4c97-8de6-a1e2cbbe5363	2018-11-15 06:00:00+00	2018-11-15 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
e5f972c6-2997-480a-8a3c-fd6705b86e3e	2018-11-16 06:00:00+00	2018-11-16 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
de78f715-2f8a-4c7e-986c-fd2201d76643	2018-11-17 06:00:00+00	2018-11-17 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
847d4918-7aea-412b-a0e1-1264ad1a88d0	2018-11-18 06:00:00+00	2018-11-18 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
f9406f69-0a4c-4eda-af67-3db7a5252c71	2018-11-19 06:00:00+00	2018-11-19 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
92007747-81e3-4d10-bdf6-c4da875e6842	2018-11-20 06:00:00+00	2018-11-20 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
f2853086-7b79-4477-98c9-a36ce4abe2f8	2018-11-21 06:00:00+00	2018-11-21 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
6648ccc3-ac5f-40cf-83b9-c6932a80b1f3	2018-11-22 06:00:00+00	2018-11-22 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
4307611d-4469-4f55-b094-8ffe57dce083	2018-11-23 06:00:00+00	2018-11-23 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
1253a760-f60c-46fb-a7c5-00a2b6d1ca75	2018-11-24 06:00:00+00	2018-11-24 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
6d42a76f-9370-4024-8458-7daca68f9b48	2018-11-25 06:00:00+00	2018-11-25 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
e3cbebd8-b02a-48ea-83a8-1b0d3a0371cd	2018-11-26 06:00:00+00	2018-11-26 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
a101c640-5d72-4df6-abbf-4f5ccd8ab0a8	2018-11-27 06:00:00+00	2018-11-27 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
3d7822b4-d1ac-4c71-90c0-7aebeca4e2bf	2018-10-16 09:00:00+00	2018-10-16 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
3b86a464-edf2-47ed-a849-0fea5eb230ba	2018-10-18 09:00:00+00	2018-10-18 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
129af7e8-b6ca-4f71-9970-d216723d5dcc	2018-10-20 09:00:00+00	2018-10-20 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
2fad5719-4824-48ba-a97e-e7a2acb4871c	2018-10-22 09:00:00+00	2018-10-22 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
d645330c-4b7c-42e5-a199-530027b19f93	2018-10-26 09:00:00+00	2018-10-26 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
34ffb5d3-accc-4d41-8d1e-8b393898c53b	2018-10-28 09:00:00+00	2018-10-28 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
a7716f3e-cbb2-4563-a84a-1299f3cc6c19	2018-10-30 09:00:00+00	2018-10-30 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
cccc0713-eb67-4ac8-9def-bdc6d2e9e159	2018-11-01 09:00:00+00	2018-11-01 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
cfec8ab5-1d35-4c93-86fd-d54c3387cade	2018-11-03 09:00:00+00	2018-11-03 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
45521dad-01d1-4cf8-aa36-149a93dcf7e9	2018-11-05 09:00:00+00	2018-11-05 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
0dcf88d4-ebb9-4908-8db1-47769c7185de	2018-11-07 09:00:00+00	2018-11-07 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
a0467bbe-9a2a-4666-937b-0035fdbcd7eb	2018-11-09 09:00:00+00	2018-11-09 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
80182ee1-e515-4d8b-b806-f8d3e942c5bd	2018-11-11 09:00:00+00	2018-11-11 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
ff16f2d8-0576-4fa9-8178-95d2cddb67a6	2018-11-13 09:00:00+00	2018-11-13 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
aff34b44-c59c-4265-9f2d-66ddbfd49221	2018-11-15 09:00:00+00	2018-11-15 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
e4748ccf-0b4a-443d-a7a3-c793d1743a46	2018-11-17 09:00:00+00	2018-11-17 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
2416cceb-0bbf-4641-9ccf-dda8773dd651	2018-11-19 09:00:00+00	2018-11-19 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
0189883f-6413-4206-a4bd-6618c8f147fc	2018-11-21 09:00:00+00	2018-11-21 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
2cbe8f1f-0993-46f0-9822-bc5d715c9384	2018-11-23 09:00:00+00	2018-11-23 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
c2392520-f148-4929-918a-082b9eef5ad8	2018-11-25 09:00:00+00	2018-11-25 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
8f5a07a9-473c-4abd-b1f5-561d1473f4e7	2018-11-27 09:00:00+00	2018-11-27 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
4a8dd415-a27a-410c-8f19-e18d03466e6a	2018-10-24 09:00:00+00	2018-10-24 17:00:00+00	done	ca176f3f-2425-4b38-ab30-bfa62a33f65b	a52bdf43-4e23-4d89-a931-cb36e6979a12
53346160-f500-449b-8caa-3265a6de0926	2018-10-17 16:00:00+00	2018-10-17 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
cb3157ec-a9ed-4337-a296-238eaa6c2228	2018-10-18 16:00:00+00	2018-10-18 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
0b7b065b-05f7-46c7-89dc-e7a91a69c3a7	2018-10-16 06:00:00+00	2018-10-16 10:00:00+00	missed	c93cd17c-e660-4801-a266-609237398341	fdb25787-150f-4117-a757-b1cd399b98f3
37a3c1b7-ad98-4c51-acbf-2c6f82568e97	2018-10-16 11:00:00+00	2018-10-16 02:00:00+00	done	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
daff962b-2de5-4dd7-80db-d74816e634be	2018-10-19 16:00:00+00	2018-10-19 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
2b88e84f-67bb-4773-8c2a-7266d3965957	2018-10-20 16:00:00+00	2018-10-20 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
c96d321f-a8cd-4c7a-8be4-296e20cabf5e	2018-10-21 16:00:00+00	2018-10-21 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
22f9a106-4f81-4111-85ec-40ec852864ed	2018-10-22 16:00:00+00	2018-10-22 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
8f806076-5afd-453c-ad74-bb24da12e34f	2018-10-23 16:00:00+00	2018-10-23 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
4ecb9d13-8923-41de-93cc-b3881ec4f9d4	2018-10-24 16:00:00+00	2018-10-24 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
21d85166-1dc6-4e67-b2bf-f605da072c48	2018-10-25 16:00:00+00	2018-10-25 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
a914fd0a-c220-4e87-896f-6a6cadd37899	2018-10-26 16:00:00+00	2018-10-26 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
d9992f65-e226-473c-8261-761c068ea54a	2018-10-27 16:00:00+00	2018-10-27 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
e86c0978-17b5-4d76-940e-29e6dcb42864	2018-10-28 16:00:00+00	2018-10-28 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
1b2aa27e-30e7-466c-9281-494ed8146640	2018-10-29 16:00:00+00	2018-10-29 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
93d35927-f51c-4c08-a163-9cc95d29770d	2018-10-30 16:00:00+00	2018-10-30 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
11212e18-5039-4575-aeea-39e1e9870ea8	2018-10-31 16:00:00+00	2018-10-31 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
71bc4fa6-6519-4cce-b0c7-e0b42d492b65	2018-11-01 16:00:00+00	2018-11-01 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
ee8694f0-ae39-42e5-ac40-2c7fd1f091bb	2018-11-02 16:00:00+00	2018-11-02 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
0b41479e-82d2-44a6-bd66-3c36d868165c	2018-11-03 16:00:00+00	2018-11-03 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
cdb6a76d-cb6b-47ce-99e7-9daf9ce704bc	2018-11-04 16:00:00+00	2018-11-04 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
2ae231ef-f82b-4e1a-8608-931fc10c608a	2018-11-05 16:00:00+00	2018-11-05 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
0dd7b0f6-99d2-41dd-93c2-fa713d774f52	2018-11-06 16:00:00+00	2018-11-06 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
aa7a068d-9268-49d0-a9fb-b14f0cfdc8e2	2018-11-07 16:00:00+00	2018-11-07 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
0264ef1a-8465-43bc-aa6c-17c182b05fbf	2018-11-08 16:00:00+00	2018-11-08 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
4090952b-478a-4060-8968-1b57502cdc70	2018-11-09 16:00:00+00	2018-11-09 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
61bd99f7-079c-4740-a131-30aa395ce423	2018-11-10 16:00:00+00	2018-11-10 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
dc73b238-776d-4bf7-abfd-349650257cb9	2018-11-11 16:00:00+00	2018-11-11 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
69077648-ab18-4aaa-ad71-7580a29c1b38	2018-11-12 16:00:00+00	2018-11-12 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
89781ac8-4338-408d-9994-385503cc0456	2018-11-13 16:00:00+00	2018-11-13 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
87126979-8bf4-4d1b-a854-0c939812a94a	2018-11-14 16:00:00+00	2018-11-14 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
121f1607-b5b9-493f-b106-899b4466b972	2018-11-15 16:00:00+00	2018-11-15 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
83a754d0-cfe2-47bf-854d-166b0d104573	2018-11-16 16:00:00+00	2018-11-16 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
9db760e7-2851-4b50-810c-409cb965d7bf	2018-11-17 16:00:00+00	2018-11-17 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
6d36e77a-ec97-4c1c-a3c5-479be345de76	2018-11-18 16:00:00+00	2018-11-18 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
a5c41b9c-0dce-4763-b36d-6f95978319ec	2018-11-19 16:00:00+00	2018-11-19 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
43d13fa5-758a-432d-8a20-cf6e135fb980	2018-11-20 16:00:00+00	2018-11-20 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
7222f124-bf25-4c02-8628-ece15cce632c	2018-11-21 16:00:00+00	2018-11-21 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
b9fda7e1-e750-45ac-a781-5d23aa7c05b3	2018-11-22 16:00:00+00	2018-11-22 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
b8c1976b-cd63-479c-bd41-d967b92bd512	2018-11-23 16:00:00+00	2018-11-23 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
7bd83525-4fcf-4d59-8450-936a05ced58d	2018-11-24 16:00:00+00	2018-11-24 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
f546c2fb-78af-4fe6-ac4b-d126bfae6d39	2018-11-25 16:00:00+00	2018-11-25 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
ce90b5ab-8259-48de-a4fe-f273367e102a	2018-11-26 16:00:00+00	2018-11-26 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
b33d3f35-a278-46cc-85b6-e255b0fcb7a2	2018-11-27 16:00:00+00	2018-11-27 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
3894f9b7-c099-4455-b887-fb8b7ef8fcf1	2018-11-28 16:00:00+00	2018-11-28 20:00:00+00	undefined	444eb230-19e1-45da-86db-b5421e3bb1f0	c222e159-26f4-4bd6-9ea5-863f0cb0df71
22d513f6-336c-4f5a-9848-bd296c4d474a	2018-10-17 11:00:00+00	2018-10-17 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
c2c3ff91-d4ad-440f-9677-989732a48000	2018-10-18 11:00:00+00	2018-10-18 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
985de88e-4032-4cce-ab43-2b91454e67ff	2018-10-19 11:00:00+00	2018-10-19 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
8aedc0ff-f59d-42a4-9600-da7739534477	2018-10-20 11:00:00+00	2018-10-20 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
95f3536f-775d-40fb-98e6-7d7af77cff56	2018-10-21 11:00:00+00	2018-10-21 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
724b422c-eae0-41b9-930c-316f87506df3	2018-10-22 11:00:00+00	2018-10-22 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
4a59f287-71c4-45e9-b066-181c22c6db64	2018-10-23 11:00:00+00	2018-10-23 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
b86d82c3-c8e0-41a7-be07-fce297debbfd	2018-10-24 11:00:00+00	2018-10-24 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
f67bbb97-0b20-411a-9367-6c127e28ac4f	2018-10-25 11:00:00+00	2018-10-25 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
7b00992a-dbf6-41c3-ac85-6f83c0498402	2018-10-26 11:00:00+00	2018-10-26 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
f37d603d-55ec-45cc-937c-40e4d9001172	2018-10-27 11:00:00+00	2018-10-27 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
d08a7ee4-024f-4f20-8f0f-b89a46b96ea6	2018-10-28 11:00:00+00	2018-10-28 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
169c8e58-10dd-40e9-a74a-03dd5189a7b9	2018-10-29 11:00:00+00	2018-10-29 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
58e7f3db-2082-4819-a290-5cfe80c8b3c3	2018-10-30 11:00:00+00	2018-10-30 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
264fae90-fcc3-4e16-bc0a-e323c9668a6c	2018-10-31 11:00:00+00	2018-10-31 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
15eb1ba2-8c90-4b2c-9e20-9c250a47c863	2018-11-01 11:00:00+00	2018-11-01 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
f93322e1-73c7-46b1-b312-c663d4a2f19a	2018-11-02 11:00:00+00	2018-11-02 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
35f3cf84-a81c-4e41-8707-c2c1374975ba	2018-11-03 11:00:00+00	2018-11-03 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
c6697476-e6f0-41e0-ac79-50e909ea4605	2018-11-04 11:00:00+00	2018-11-04 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
846a02b4-906b-46aa-9093-de17b9a9ebf6	2018-11-05 11:00:00+00	2018-11-05 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
52188d4b-5905-4131-9fdf-a32befa08e59	2018-11-06 11:00:00+00	2018-11-06 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
13820f83-1750-46b4-8b58-e82658f1490f	2018-11-07 11:00:00+00	2018-11-07 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
681ea08d-5ca1-4c8c-881b-c897fd68e57f	2018-11-08 11:00:00+00	2018-11-08 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
f825e356-80db-4cb2-916c-8231e3194466	2018-11-09 11:00:00+00	2018-11-09 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
4e891663-dd60-47b4-9cb1-84e89158365c	2018-11-10 11:00:00+00	2018-11-10 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
26617ae2-6c99-459f-841d-e87cd16a2189	2018-11-11 11:00:00+00	2018-11-11 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
716ddcae-19a5-46cf-92ba-e6c5e3c9de18	2018-11-12 11:00:00+00	2018-11-12 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
94869f4b-d397-446d-b097-34ed52cbe593	2018-11-13 11:00:00+00	2018-11-13 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
f88b4f64-586e-4662-9537-953bf32df32a	2018-11-14 11:00:00+00	2018-11-14 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
689f1603-69ab-4ced-82b5-5f1fb96c9044	2018-11-15 11:00:00+00	2018-11-15 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
4a28e3f4-d17c-4641-9d4a-4ec7ede88db2	2018-11-16 11:00:00+00	2018-11-16 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
43fc4e01-d619-4714-8cec-389bb45a1a7c	2018-11-17 11:00:00+00	2018-11-17 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
986ef829-dfd4-40d1-b82e-e64e84d65162	2018-11-18 11:00:00+00	2018-11-18 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
f8630415-65bf-40a5-8c22-64c89ef7903f	2018-11-19 11:00:00+00	2018-11-19 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
77e4ed9c-f672-4a45-b621-4de6c0593e67	2018-11-20 11:00:00+00	2018-11-20 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
69ddd62e-48fc-440c-bc8a-824248773933	2018-11-21 11:00:00+00	2018-11-21 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
0a1ff674-9fe4-40a7-ab6d-92ae7b17dc3a	2018-11-22 11:00:00+00	2018-11-22 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
198c5791-033a-44c4-99ba-c103295d8c82	2018-11-23 11:00:00+00	2018-11-23 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
50616a82-ac00-4d74-878f-9d5a9fee96d2	2018-11-24 11:00:00+00	2018-11-24 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
2e3827f2-8154-4ef0-be86-105926ec80fe	2018-11-25 11:00:00+00	2018-11-25 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
b3bf684f-c76a-4498-b19a-ae3df713f35a	2018-11-26 11:00:00+00	2018-11-26 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
e496861b-f902-4685-bb87-a991e7fdfb9e	2018-11-27 11:00:00+00	2018-11-27 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
e5897398-0c98-4e9d-a566-eba0ac96c606	2018-11-28 11:00:00+00	2018-11-28 02:00:00+00	undefined	58fe54a7-c309-44c2-a385-30dfb26de16e	c222e159-26f4-4bd6-9ea5-863f0cb0df71
6e9ee9c0-75a2-4d79-9972-370915d24147	2018-10-17 06:00:00+00	2018-10-17 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
4356f537-4597-4220-b8ec-60caf85e19db	2018-10-18 06:00:00+00	2018-10-18 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
ad35385c-c544-44e5-8c1f-6e13d62fa174	2018-10-19 06:00:00+00	2018-10-19 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
25d0978f-bf5c-4b4f-a4a7-02041998dfd3	2018-10-20 06:00:00+00	2018-10-20 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
8a4313ea-e576-4494-bbc4-a817320d6e08	2018-10-21 06:00:00+00	2018-10-21 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
c2ddecb4-fbbe-47af-83ba-f66745da2f2b	2018-10-22 06:00:00+00	2018-10-22 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
8c3891f1-5db6-4731-94de-ea491e32d8c1	2018-10-23 06:00:00+00	2018-10-23 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
af07ec29-9625-4061-9a52-0b9eb33eee7a	2018-10-24 06:00:00+00	2018-10-24 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
27381f46-5cba-4615-a662-fe17038006a8	2018-10-25 06:00:00+00	2018-10-25 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
cc92f14a-4207-4e51-b68a-3c59bf1f872e	2018-10-26 06:00:00+00	2018-10-26 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
d43ccd05-fcbe-4c75-a74a-dff9433afe7d	2018-10-27 06:00:00+00	2018-10-27 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
9f1bc32a-2135-49aa-98b0-0aa4da74b8fd	2018-10-28 06:00:00+00	2018-10-28 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
65cc82ec-86fe-4d53-a7ba-7b9033cfe4a8	2018-10-29 06:00:00+00	2018-10-29 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
b65e327d-01d3-4278-846d-998f748d9fff	2018-10-30 06:00:00+00	2018-10-30 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
6a973a69-6c7b-49c6-9e8e-522ad9c6e7b5	2018-10-31 06:00:00+00	2018-10-31 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
087a3c9d-2b1f-44bf-8f93-7f4e88513c54	2018-11-01 06:00:00+00	2018-11-01 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
007940cd-bad8-45e3-b0ff-fd5100db392d	2018-11-02 06:00:00+00	2018-11-02 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
4d973e24-7c51-4d94-9159-4bc401df56f5	2018-11-03 06:00:00+00	2018-11-03 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
acb24bf6-a976-4602-9102-8c8eba90390b	2018-11-04 06:00:00+00	2018-11-04 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
ac040774-c1eb-4a77-abe6-ec6b0d72da01	2018-11-05 06:00:00+00	2018-11-05 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
0c0b574f-5070-4f2a-9d69-1dd18ef08b9e	2018-11-06 06:00:00+00	2018-11-06 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
64074ac1-04f7-47d6-ac26-2589489459dc	2018-11-07 06:00:00+00	2018-11-07 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
824c14c6-388e-4310-b3e6-d8a6d8b6c8ea	2018-11-08 06:00:00+00	2018-11-08 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
2b8ec416-6f65-4d21-8c58-fc4abbb17692	2018-11-09 06:00:00+00	2018-11-09 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
5fbf0f88-ec3b-43c3-9558-b49ef8d5f3a9	2018-11-10 06:00:00+00	2018-11-10 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
77141a6f-a6e9-4b6c-a778-6351a17643ce	2018-11-11 06:00:00+00	2018-11-11 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
3b899f9b-42d7-4eac-9799-d3c265aee7cb	2018-11-12 06:00:00+00	2018-11-12 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
4def7b5d-1ea9-4e0a-9735-255713c7d8ad	2018-11-13 06:00:00+00	2018-11-13 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
1ad2b7ab-7ddc-4a73-a021-65c8addacfdc	2018-11-14 06:00:00+00	2018-11-14 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
740ccbc0-4ce7-4dad-b51f-c7e634796e43	2018-11-15 06:00:00+00	2018-11-15 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
ece9fa5e-bd5f-4bff-9457-510ef5bfe27e	2018-11-16 06:00:00+00	2018-11-16 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
92b406c7-b8e6-436d-b92d-cba79dd589fa	2018-11-17 06:00:00+00	2018-11-17 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
dbc9e771-9e2d-44ec-8103-4be740cbd27f	2018-11-18 06:00:00+00	2018-11-18 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
f3296096-5596-4757-857c-5b0ec91990bf	2018-11-19 06:00:00+00	2018-11-19 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
e0e0dc9d-d11d-46fc-a9c9-77ad76b4457a	2018-11-20 06:00:00+00	2018-11-20 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
3f2faa4b-edd0-4b21-a78f-05347294ba28	2018-11-21 06:00:00+00	2018-11-21 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
23a4b728-8e53-4d32-bb41-588edbefc754	2018-11-22 06:00:00+00	2018-11-22 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
2274759e-9a4a-472d-b117-923ca187929a	2018-11-23 06:00:00+00	2018-11-23 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
11113481-fe2a-4272-8e1f-9e477396e2f9	2018-11-24 06:00:00+00	2018-11-24 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
60aa2cb0-14f9-4928-9785-872182b4ddcb	2018-11-25 06:00:00+00	2018-11-25 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
01437fe5-7b4d-40d9-977f-4e8c01dd30b1	2018-11-26 06:00:00+00	2018-11-26 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
73769a41-8d81-4719-a9fc-f4a580e2f98a	2018-11-27 06:00:00+00	2018-11-27 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
b8bdfc84-2406-4c9c-8f6e-2bcb5382f0cc	2018-11-28 06:00:00+00	2018-11-28 10:00:00+00	undefined	c93cd17c-e660-4801-a266-609237398341	c222e159-26f4-4bd6-9ea5-863f0cb0df71
c77ce66d-5908-4462-912c-70317f39126c	2018-10-17 09:00:00+00	2018-10-17 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
dd530f54-2c76-4bf0-a5ba-cf565fcc3ea1	2018-10-19 09:00:00+00	2018-10-19 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
95ec9e9a-6ed1-47dc-9a32-7156ad1b2c41	2018-10-21 09:00:00+00	2018-10-21 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
915568ee-dfa8-4d94-8f67-68aaaf1df961	2018-10-23 09:00:00+00	2018-10-23 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
2d82ce1b-1621-40b4-a8c0-b56f5850d3b2	2018-10-25 09:00:00+00	2018-10-25 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
2718f399-dfd7-418a-8ad2-6b82dd89b64e	2018-10-27 09:00:00+00	2018-10-27 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
043031e6-4890-4b1a-8792-53013348eb1d	2018-10-29 09:00:00+00	2018-10-29 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
8c866477-8c85-4e0c-ae93-1bc5ab8adaef	2018-10-31 09:00:00+00	2018-10-31 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
cbf9fb6b-7a16-4097-84df-481fd0c3bc63	2018-11-02 09:00:00+00	2018-11-02 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
a887f489-6faf-4ed4-b64e-ed9dd96d1b8c	2018-11-04 09:00:00+00	2018-11-04 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
7db7c45b-81ac-4835-991e-492a1a03db94	2018-11-06 09:00:00+00	2018-11-06 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
afe49f32-3fdf-4f2e-8577-c504e58bd736	2018-11-08 09:00:00+00	2018-11-08 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
4a2c57c3-b22d-40ac-9e5d-069da1318720	2018-11-10 09:00:00+00	2018-11-10 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
6c950496-5702-4a21-bd0c-421cb4eb168e	2018-11-12 09:00:00+00	2018-11-12 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
70dc722c-b44b-4f8a-82d0-dfda50591d29	2018-11-14 09:00:00+00	2018-11-14 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
a3ce4787-e280-4d06-9015-51183214894f	2018-11-16 09:00:00+00	2018-11-16 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
0cac1e90-dc97-431d-89d5-02d2a1fea30a	2018-11-18 09:00:00+00	2018-11-18 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
b60da0c2-f56d-4f7e-91db-bae297bee546	2018-11-20 09:00:00+00	2018-11-20 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
bc22b1ed-12a4-4a88-97aa-a90bc592b6d8	2018-11-22 09:00:00+00	2018-11-22 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
152cc998-1406-42bc-9ab9-95e6bf338ddb	2018-11-24 09:00:00+00	2018-11-24 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
560eeaa1-ec5c-4fe2-a985-1eca4caf93c0	2018-11-26 09:00:00+00	2018-11-26 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
551d5364-1545-4137-ada6-3ad8e9d78d4e	2018-11-28 09:00:00+00	2018-11-28 17:00:00+00	undefined	ca176f3f-2425-4b38-ab30-bfa62a33f65b	c222e159-26f4-4bd6-9ea5-863f0cb0df71
06ed8a55-2de7-48bd-a9a5-2eed2b9b042a	2018-10-23 09:00:00+00	2018-10-23 17:00:00+00	done	ca176f3f-2425-4b38-ab30-bfa62a33f65b	fdb25787-150f-4117-a757-b1cd399b98f3
3f891cce-0ab0-4638-9c83-c051771edf7f	2018-10-23 11:00:00+00	2018-10-23 02:00:00+00	done	58fe54a7-c309-44c2-a385-30dfb26de16e	fdb25787-150f-4117-a757-b1cd399b98f3
f09e230e-6bbe-49af-8a7b-f0917d122262	2018-10-24 16:00:00+00	2018-10-24 20:00:00+00	done	444eb230-19e1-45da-86db-b5421e3bb1f0	a52bdf43-4e23-4d89-a931-cb36e6979a12
872c2ee2-6009-4908-8cb9-afa6c4a65dbe	2018-10-24 06:00:00+00	2018-10-24 10:00:00+00	done	c93cd17c-e660-4801-a266-609237398341	a52bdf43-4e23-4d89-a931-cb36e6979a12
\.


--
-- Data for Name: tasks_patienttasktemplate; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_patienttasktemplate (id, start_on_day, frequency, repeat_amount, appear_time, due_time, name, plan_template_id) FROM stdin;
ca176f3f-2425-4b38-ab30-bfa62a33f65b	0	every_other_day	-1	09:00:00	17:00:00	Call Doctor	719563fb-6394-47b8-89e0-3f6f4fad9c9f
c93cd17c-e660-4801-a266-609237398341	0	daily	-1	06:00:00	10:00:00	Eat Breakfast	719563fb-6394-47b8-89e0-3f6f4fad9c9f
444eb230-19e1-45da-86db-b5421e3bb1f0	0	daily	-1	16:00:00	20:00:00	Eat Dinner	719563fb-6394-47b8-89e0-3f6f4fad9c9f
58fe54a7-c309-44c2-a385-30dfb26de16e	0	daily	-1	11:00:00	02:00:00	Eat Lunch	719563fb-6394-47b8-89e0-3f6f4fad9c9f
\.


--
-- Data for Name: tasks_symptomrating; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_symptomrating (id, rating, symptom_id, symptom_task_id, created, modified) FROM stdin;
99f41f8d-2bde-4b66-91c8-b241395b51f7	3	a344d800-55b3-4853-83cb-1c814a75a9c2	810b3d1e-1f85-4763-b9d5-63e1f4a10e4e	2018-10-24 19:41:42.039917+00	2018-10-24 19:41:42.080618+00
0ffe520f-633f-4336-b8f4-bf976c47b4bc	3	a344d800-55b3-4853-83cb-1c814a75a9c2	ae7d1207-9e33-4181-9112-b9b17f81026a	2018-10-24 19:41:42.039917+00	2018-10-24 19:41:42.080618+00
2faaa68b-e9ad-4c1b-9082-e3ba48bef91b	4	0c3bf862-ca7c-42d6-9d42-6b7995919973	ae7d1207-9e33-4181-9112-b9b17f81026a	2018-10-24 19:41:42.039917+00	2018-10-24 19:41:42.080618+00
3419c121-7556-4664-9e12-02d5da8846da	1	a344d800-55b3-4853-83cb-1c814a75a9c2	5f2f78db-11be-4626-ad52-0caba6587df0	2018-10-24 19:41:42.039917+00	2018-10-24 19:41:42.080618+00
a62bc65a-5fb4-486b-b702-daf24a46b353	4	0c3bf862-ca7c-42d6-9d42-6b7995919973	5f2f78db-11be-4626-ad52-0caba6587df0	2018-10-24 19:41:42.039917+00	2018-10-24 19:41:42.080618+00
a82e2eee-a56c-4931-a848-0c9696689cba	1	a344d800-55b3-4853-83cb-1c814a75a9c2	5f2f78db-11be-4626-ad52-0caba6587df0	2018-10-24 19:41:42.039917+00	2018-10-24 19:41:42.080618+00
988500b3-5261-41d4-a246-09e2438f4afc	4	0c3bf862-ca7c-42d6-9d42-6b7995919973	5f2f78db-11be-4626-ad52-0caba6587df0	2018-10-24 19:41:42.039917+00	2018-10-24 19:41:42.080618+00
670ba5e1-77bb-46ee-a64f-6751e534ff50	5	a344d800-55b3-4853-83cb-1c814a75a9c2	904923d9-3e22-4e79-8565-d168680ea660	2018-10-24 20:00:19.996196+00	2018-10-24 20:00:19.996215+00
c21b67e6-361b-4b41-8439-3d2baa63115e	4	a344d800-55b3-4853-83cb-1c814a75a9c2	900a4db6-885c-4694-a1af-a94d06482acc	2018-10-24 20:00:35.226468+00	2018-10-24 20:00:35.226487+00
1cc28df0-4a13-42fd-aa83-ecd4aa4aecb3	5	0c3bf862-ca7c-42d6-9d42-6b7995919973	904923d9-3e22-4e79-8565-d168680ea660	2018-10-24 20:01:18.769316+00	2018-10-24 20:01:18.769334+00
7a1c4544-4600-41d5-88cb-e91c349b3f59	4	0c3bf862-ca7c-42d6-9d42-6b7995919973	900a4db6-885c-4694-a1af-a94d06482acc	2018-10-24 20:01:25.340466+00	2018-10-24 20:01:25.340485+00
1bbb1b1b-1522-4436-85ec-663e5726d524	3	a344d800-55b3-4853-83cb-1c814a75a9c2	c6fbda29-dcb4-430c-b5e7-69e455ecd378	2018-10-24 20:01:32.004399+00	2018-10-24 20:01:32.004418+00
879a684d-09e1-4d9b-92ae-8d5eb3847440	3	0c3bf862-ca7c-42d6-9d42-6b7995919973	c6fbda29-dcb4-430c-b5e7-69e455ecd378	2018-10-24 20:01:32.006351+00	2018-10-24 20:01:32.006368+00
5c81002c-1300-4e34-a2fa-9a28f35a0e52	2	a344d800-55b3-4853-83cb-1c814a75a9c2	ad072c55-516d-4972-ac51-8f7fca2ac486	2018-10-24 20:01:40.472869+00	2018-10-24 20:01:40.472886+00
2b70b606-ece7-4834-a41f-f11be88e142a	2	0c3bf862-ca7c-42d6-9d42-6b7995919973	ad072c55-516d-4972-ac51-8f7fca2ac486	2018-10-24 20:01:40.474711+00	2018-10-24 20:01:40.474728+00
41f229fc-8ba8-47e4-aa9b-0e39a9e31cf9	1	a344d800-55b3-4853-83cb-1c814a75a9c2	81ba7a15-7a3d-4ff9-9d03-01bf87a3cf1a	2018-10-24 20:01:47.571362+00	2018-10-24 20:01:47.571379+00
29a793f8-a406-4a46-81aa-9ef647479110	1	0c3bf862-ca7c-42d6-9d42-6b7995919973	81ba7a15-7a3d-4ff9-9d03-01bf87a3cf1a	2018-10-24 20:01:47.573262+00	2018-10-24 20:01:47.573278+00
58f6d00b-0e78-4f45-a56d-dcd9bd0fa340	2	a344d800-55b3-4853-83cb-1c814a75a9c2	8109432b-9d74-4632-abfe-42fb0c7fa454	2018-10-24 20:02:03.577237+00	2018-10-24 20:02:03.577254+00
a96e31cf-9f0d-4dd2-8a2f-21e0071a264e	2	0c3bf862-ca7c-42d6-9d42-6b7995919973	8109432b-9d74-4632-abfe-42fb0c7fa454	2018-10-24 20:02:03.579162+00	2018-10-24 20:02:03.57918+00
86cf605c-bc41-4af3-bb40-27de46aec972	2	a344d800-55b3-4853-83cb-1c814a75a9c2	354037dc-b621-4597-b861-99b6dadddd9e	2018-10-24 20:05:30.759865+00	2018-10-24 20:05:30.759883+00
21224282-5aeb-49d3-84d9-8aefa1350af8	3	0c3bf862-ca7c-42d6-9d42-6b7995919973	354037dc-b621-4597-b861-99b6dadddd9e	2018-10-24 20:05:30.761805+00	2018-10-24 20:05:30.761822+00
a7499bb4-866a-4415-beb0-e035334f3e2d	1	a344d800-55b3-4853-83cb-1c814a75a9c2	ae4c5e59-e4db-468f-adcc-5db7e6d7f8bd	2018-10-24 20:06:01.474163+00	2018-10-24 20:06:01.474183+00
2098824a-e342-430b-b4be-1bd69cfccf51	3	0c3bf862-ca7c-42d6-9d42-6b7995919973	ae4c5e59-e4db-468f-adcc-5db7e6d7f8bd	2018-10-24 20:06:01.476127+00	2018-10-24 20:06:01.476145+00
\.


--
-- Data for Name: tasks_symptomtask; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_symptomtask (id, appear_datetime, due_datetime, comments, plan_id, symptom_task_template_id, is_complete) FROM stdin;
201c18e5-314a-48f4-990b-bfd62dd8fcb3	2018-10-18 00:01:00+00	2018-10-18 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
7a48d501-d0d5-4801-bc8c-ccf06e2348d1	2018-10-07 00:01:00+00	2018-10-07 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
55d0b6e8-c8d9-4e53-9767-86355baf3b18	2018-10-09 00:01:00+00	2018-10-09 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
bbe1b635-0362-4a8d-943c-7f79fd5d4c97	2018-10-10 00:01:00+00	2018-10-10 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
c6686884-fa7b-4eb2-ad5b-4aaf6cbc0485	2018-10-11 00:01:00+00	2018-10-11 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
bd5ff782-3e2e-4404-82d2-e292315b0d6c	2018-10-12 00:01:00+00	2018-10-12 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
15fed89a-a09c-411c-a128-f7eb6af1b59b	2018-10-13 00:01:00+00	2018-10-13 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
195328a2-c813-485f-a536-d45d6d54a9c9	2018-10-14 00:01:00+00	2018-10-14 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f76d290a-1abf-458e-b547-91c86104fa16	2018-10-15 00:01:00+00	2018-10-15 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
e120837d-cb59-4330-bce9-83f348af1399	2018-10-16 00:01:00+00	2018-10-16 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
09559765-2251-44f7-a0be-93033e87026a	2018-10-17 00:01:00+00	2018-10-17 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f2135748-28fd-4781-881f-62b9cda43e2d	2018-10-18 00:01:00+00	2018-10-18 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
d2ce14c3-21cf-4f57-bd0c-d072b57ead47	2018-10-19 00:01:00+00	2018-10-19 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f21072d6-5a1d-4b59-a726-c3fee39ba065	2018-10-20 00:01:00+00	2018-10-20 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
05dae191-25bd-40d9-b5cb-928f1b44e61c	2018-10-21 00:01:00+00	2018-10-21 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
30552b56-87b1-4cb2-b2c1-cdc71785d438	2018-10-22 00:01:00+00	2018-10-22 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
0d8ec151-6c72-40dd-8415-78cdc22d7b47	2018-10-24 00:01:00+00	2018-10-24 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
17444d0b-d301-47a7-9fe5-95b8807dd34f	2018-10-25 00:01:00+00	2018-10-25 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f50048b1-325b-49fc-a94b-ae0a46bb63f8	2018-10-26 00:01:00+00	2018-10-26 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
752a9acc-39c7-4a81-bafd-e843a2136f07	2018-10-27 00:01:00+00	2018-10-27 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
1b97cafd-325a-4aab-866f-7a2c5f5c340b	2018-10-28 00:01:00+00	2018-10-28 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
d58621b9-5f39-4936-93a7-62b611a9edb9	2018-10-29 00:01:00+00	2018-10-29 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
32c02982-91f0-4f54-b1f7-4efaf74f13cf	2018-10-30 00:01:00+00	2018-10-30 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
029d5f6d-e968-4c7e-af59-2de53a772e1b	2018-10-31 00:01:00+00	2018-10-31 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f6d626d7-05e4-4134-90be-a3acb20b6c04	2018-11-01 00:01:00+00	2018-11-01 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
0f70f81b-b637-44a8-8cd6-7eeb560efa56	2018-11-02 00:01:00+00	2018-11-02 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
c488aab9-86de-4f55-95dd-14bd1df0b16c	2018-11-03 00:01:00+00	2018-11-03 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
31b82fff-57e8-45c0-89cb-00b0d5f62141	2018-11-04 00:01:00+00	2018-11-04 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
6e530e8d-ade4-4162-b3ab-7b3020d9f287	2018-11-05 00:01:00+00	2018-11-05 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
ddd5f6e4-df00-44d2-924f-8470bf3e99f8	2018-11-06 00:01:00+00	2018-11-06 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f8eece8e-23f3-4730-ac41-28e7694a3924	2018-11-07 00:01:00+00	2018-11-07 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
620600a6-bed4-49ed-879a-81955a01d535	2018-11-08 00:01:00+00	2018-11-08 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
dd1eccff-0c96-4cc5-b4d8-5d8ea057a329	2018-11-09 00:01:00+00	2018-11-09 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
e191d18c-cc5e-4e4e-ad24-f83ffbad3e64	2018-11-10 00:01:00+00	2018-11-10 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
53c89752-2311-4b7a-b472-000539071f9b	2018-11-11 00:01:00+00	2018-11-11 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
9339329c-aed5-4b9e-b0fa-873eb3f037a3	2018-11-12 00:01:00+00	2018-11-12 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
5f7cd329-91fa-4e88-aa1b-a976d195895c	2018-11-13 00:01:00+00	2018-11-13 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f7941222-88c6-401c-bbc3-3c054587bd5c	2018-11-14 00:01:00+00	2018-11-14 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
6f8b957a-857f-4f78-8678-186a42e5579c	2018-11-15 00:01:00+00	2018-11-15 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
da5e286f-b180-4a2e-a92e-5005474ff96d	2018-11-16 00:01:00+00	2018-11-16 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f9a59b68-5795-4a2e-b768-968e59699c7b	2018-10-19 00:01:00+00	2018-10-19 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
04e5e8a1-6203-44a0-afc6-99cd5808a14c	2018-10-20 00:01:00+00	2018-10-20 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
7bab943c-f25f-4865-9c58-b89b8fe32629	2018-10-21 00:01:00+00	2018-10-21 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
d0fe6f6e-fa2d-4a5f-80e4-bda9be3d7c96	2018-10-22 00:01:00+00	2018-10-22 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
493a676c-b069-4f6f-bcfd-45d4dac46523	2018-10-23 00:01:00+00	2018-10-23 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
ab0e2f86-6bd2-4bbf-8218-1615bd083e17	2018-10-24 00:01:00+00	2018-10-24 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
fe7689e5-d54e-4edf-af9f-ac2dc3c0a92b	2018-10-25 00:01:00+00	2018-10-25 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
e4c22bb3-e229-4e72-83e6-35093a7a0e58	2018-10-26 00:01:00+00	2018-10-26 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
19a7ed97-e8cc-4a22-abc6-6f1a6f18d7fb	2018-10-27 00:01:00+00	2018-10-27 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
4b38fa35-6570-4339-82f8-d27ce5dbf1ec	2018-10-28 00:01:00+00	2018-10-28 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
4916151d-431b-4f78-91a9-1923e723c359	2018-10-29 00:01:00+00	2018-10-29 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
3365b52a-72e9-4ff4-ae1e-b353bb369777	2018-10-30 00:01:00+00	2018-10-30 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
c5432047-b839-42f9-95ac-c1ba612dca95	2018-10-31 00:01:00+00	2018-10-31 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
e7e8d331-1c69-4789-b49d-054daf5bbdc3	2018-11-01 00:01:00+00	2018-11-01 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
852eeb63-80fd-43ec-868f-7138c41c0138	2018-11-02 00:01:00+00	2018-11-02 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
1749ce22-4492-4c48-a077-7304a58033ac	2018-11-03 00:01:00+00	2018-11-03 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
d507c931-4839-49cf-82e7-80069c100952	2018-11-04 00:01:00+00	2018-11-04 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
47588e06-0834-4a71-8235-176e5183c1e0	2018-11-05 00:01:00+00	2018-11-05 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
8e123a42-06ae-4f97-9922-bb09d7fe0b06	2018-11-06 00:01:00+00	2018-11-06 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
11a9798d-9bc3-40a1-8ef8-2f726387b9af	2018-11-07 00:01:00+00	2018-11-07 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f9c39a15-abd0-4675-b532-8fd8a86b4a38	2018-11-08 00:01:00+00	2018-11-08 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
267d2b80-d55b-446a-8f03-843da985547f	2018-11-09 00:01:00+00	2018-11-09 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
808709ea-386d-46a6-88b1-8c27b0550b08	2018-11-10 00:01:00+00	2018-11-10 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
27e4d60b-769d-4633-8b7a-7b3b4c672360	2018-11-11 00:01:00+00	2018-11-11 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
d0908baa-8e73-4fb2-b773-bf57870d04e5	2018-11-12 00:01:00+00	2018-11-12 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
4f62b040-9a24-46b7-8c74-f2a7d2526085	2018-11-13 00:01:00+00	2018-11-13 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
d5135552-53be-42e0-86f2-aa14af534085	2018-11-14 00:01:00+00	2018-11-14 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
8328ce0f-9049-416b-89dc-6efb8439f25f	2018-11-15 00:01:00+00	2018-11-15 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
4a4975b0-a6f9-4caf-9c2e-8f54276a6cd9	2018-11-16 00:01:00+00	2018-11-16 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
ae608b17-07a7-4235-8140-bc3b226f926c	2018-11-17 00:01:00+00	2018-11-17 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
1adb9892-f54e-443f-bbf0-8605663cb1fe	2018-11-18 00:01:00+00	2018-11-18 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
63071814-a6a7-4d52-87a9-ea77cd6fbe1e	2018-11-19 00:01:00+00	2018-11-19 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
4a5e39af-8f2c-4c2a-99db-34f40cdcee82	2018-11-20 00:01:00+00	2018-11-20 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
6682fe03-3130-4544-be87-a9bb67c6f3f3	2018-11-21 00:01:00+00	2018-11-21 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
a4552429-3123-4cb7-8faa-153c25195272	2018-11-22 00:01:00+00	2018-11-22 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
fa4f6651-b40f-4644-951a-2706a2592dc4	2018-11-23 00:01:00+00	2018-11-23 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
a5a975cd-ee46-4efb-8235-6b28e3154dda	2018-11-24 00:01:00+00	2018-11-24 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
1d0272c3-4bb4-469d-9ac0-be3f1349322c	2018-11-25 00:01:00+00	2018-11-25 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
beba40dc-5a55-4fe8-bcbe-807d313544ea	2018-11-26 00:01:00+00	2018-11-26 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
ae7d1207-9e33-4181-9112-b9b17f81026a	2018-10-08 00:01:00+00	2018-10-08 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
6ed854f8-9d72-4344-9a8b-c047c9829281	2018-11-27 00:01:00+00	2018-11-27 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
88fa3c3f-50c8-4a27-ab50-2708ea049410	2018-11-28 00:01:00+00	2018-11-28 23:59:59+00	\N	c222e159-26f4-4bd6-9ea5-863f0cb0df71	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
5f2f78db-11be-4626-ad52-0caba6587df0	2018-10-23 00:01:00+00	2018-10-23 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
810b3d1e-1f85-4763-b9d5-63e1f4a10e4e	2018-10-06 00:01:00+00	2018-10-06 23:59:59+00	\N	fdb25787-150f-4117-a757-b1cd399b98f3	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
8931ac5c-708b-4e15-93bb-bb2160981d4d	2018-10-26 00:01:00+00	2018-10-26 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
4acf7689-7159-47ce-aea6-ac119b0f2395	2018-10-27 00:01:00+00	2018-10-27 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f5a955df-2a91-4578-85ee-ca77bd044072	2018-10-28 00:01:00+00	2018-10-28 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
e8893eed-c9e9-4410-b3c9-2122aa9f7656	2018-10-29 00:01:00+00	2018-10-29 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
9da17957-9c34-41cf-bd7c-9abab815ca99	2018-10-30 00:01:00+00	2018-10-30 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
be9d2281-384d-4303-afb2-886611ae57d8	2018-10-31 00:01:00+00	2018-10-31 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
f1d0c47a-ac8e-4dbb-b416-b986672abdcd	2018-11-01 00:01:00+00	2018-11-01 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
05dbb342-763f-4044-b4d4-ba70930b53e0	2018-11-02 00:01:00+00	2018-11-02 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
81eb62a2-fabb-4c69-b399-d8e851334caa	2018-11-03 00:01:00+00	2018-11-03 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
7fb54199-4c82-49b7-8811-70c65ac20a41	2018-11-04 00:01:00+00	2018-11-04 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
1efd1932-28e5-4bd8-884f-d493773f97b4	2018-11-05 00:01:00+00	2018-11-05 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
c364a6b5-b367-4c32-adcc-49d9536cd507	2018-11-06 00:01:00+00	2018-11-06 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
e552ac08-dd06-4fa7-ae0e-1dd96044394a	2018-11-07 00:01:00+00	2018-11-07 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
cdb5d949-9a2d-4843-b2af-75bb79322a9c	2018-11-08 00:01:00+00	2018-11-08 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
5ad1467a-70d6-49c2-8e04-622a3fa60e37	2018-11-09 00:01:00+00	2018-11-09 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
6be981b0-63b1-4f39-a042-dbefd1180648	2018-11-10 00:01:00+00	2018-11-10 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
d5c8a051-23e3-449e-b8dc-cb3ca165a110	2018-11-11 00:01:00+00	2018-11-11 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
fb377332-3f29-414a-92e4-fed875e65e5e	2018-11-12 00:01:00+00	2018-11-12 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
e8fbc91e-e733-41e7-95a0-ca34a8b22deb	2018-11-13 00:01:00+00	2018-11-13 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
0571a908-a339-4334-bad3-69fd3b77ae1b	2018-11-14 00:01:00+00	2018-11-14 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
3870817a-c1fb-429c-b714-00a8405dd3c8	2018-11-15 00:01:00+00	2018-11-15 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
726684ad-3af7-451b-8881-4606d53e21b0	2018-11-16 00:01:00+00	2018-11-16 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
143b2865-7ae3-43e9-aadd-de87b00dadec	2018-11-17 00:01:00+00	2018-11-17 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
b8869235-056a-4b44-b297-bfb020fd5bd5	2018-11-18 00:01:00+00	2018-11-18 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
30382ab4-b276-4534-9a93-140d61d8fa00	2018-11-19 00:01:00+00	2018-11-19 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
e69121b4-1497-47b9-9dcf-37979bd0fd6a	2018-11-20 00:01:00+00	2018-11-20 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
408a1568-bfb4-4670-8e6b-d9a2f598af1e	2018-11-21 00:01:00+00	2018-11-21 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
a29516dd-b64e-486c-874d-1b5797c83ae8	2018-11-22 00:01:00+00	2018-11-22 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
e7ad0a4e-ccc7-4959-95c2-58f142e9865a	2018-11-23 00:01:00+00	2018-11-23 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
69ff1a5e-9827-4592-869c-44f46edf9563	2018-11-24 00:01:00+00	2018-11-24 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
0d9cf2e8-c46e-41b6-b5c3-11a2279923db	2018-11-25 00:01:00+00	2018-11-25 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
766ee7e7-26ae-4337-9c01-a29bd122e1bc	2018-11-26 00:01:00+00	2018-11-26 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
8d8b0072-4cc1-407d-bbf7-3d056040b808	2018-11-27 00:01:00+00	2018-11-27 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
b4ceb27d-5ca9-4fc8-97b4-79d9b754effc	2018-10-25 00:01:00+00	2018-10-25 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	f
904923d9-3e22-4e79-8565-d168680ea660	2018-10-17 00:01:00+00	2018-10-17 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
900a4db6-885c-4694-a1af-a94d06482acc	2018-10-18 00:01:00+00	2018-10-18 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
c6fbda29-dcb4-430c-b5e7-69e455ecd378	2018-10-19 00:01:00+00	2018-10-19 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
ad072c55-516d-4972-ac51-8f7fca2ac486	2018-10-20 00:01:00+00	2018-10-20 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
81ba7a15-7a3d-4ff9-9d03-01bf87a3cf1a	2018-10-21 00:01:00+00	2018-10-21 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
354037dc-b621-4597-b861-99b6dadddd9e	2018-10-23 00:01:00+00	2018-10-23 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
8109432b-9d74-4632-abfe-42fb0c7fa454	2018-10-22 00:01:00+00	2018-10-22 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
ae4c5e59-e4db-468f-adcc-5db7e6d7f8bd	2018-10-24 00:01:00+00	2018-10-24 23:59:59+00	\N	a52bdf43-4e23-4d89-a931-cb36e6979a12	91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	t
\.


--
-- Data for Name: tasks_symptomtasktemplate; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_symptomtasktemplate (id, start_on_day, frequency, repeat_amount, appear_time, due_time, plan_template_id) FROM stdin;
91b2e9bd-8a43-4b84-b436-e2e8f4ab49fe	1	daily	-1	00:01:00	23:59:59	719563fb-6394-47b8-89e0-3f6f4fad9c9f
\.


--
-- Data for Name: tasks_teamtask; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_teamtask (id, appear_datetime, due_datetime, plan_id, team_task_template_id, status) FROM stdin;
8c71b359-c2ad-4428-a34a-9c7ed3ebcdfe	2018-10-05 10:41:00+00	2018-10-05 00:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
a331384e-77d6-4f93-9806-7d8f7f3da8b6	2018-10-12 10:41:00+00	2018-10-12 00:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
a4e42c83-df95-4c50-b23f-0feb9c3d6f84	2018-10-19 10:41:00+00	2018-10-19 00:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
350f1ae7-ec68-4684-a4f0-cbc38ead63ec	2018-10-26 10:41:00+00	2018-10-26 00:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
920bac01-604f-4f31-8bba-349ac0f9619b	2018-11-02 10:41:00+00	2018-11-02 00:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
3339fbbd-85e4-4dd7-80d8-e65413e7293d	2018-11-09 10:41:00+00	2018-11-09 00:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
cffc7f77-016b-4b4b-a50a-7294c6017b7e	2018-11-16 10:41:00+00	2018-11-16 00:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
efc5d395-8138-4da0-94bb-039d2d64b823	2018-10-05 08:44:00+00	2018-10-05 09:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	476e62b4-d63a-4060-97a3-626a353c771f	undefined
937182e2-8905-4451-80d1-e8282eafed35	2018-10-06 08:44:00+00	2018-10-06 09:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	476e62b4-d63a-4060-97a3-626a353c771f	undefined
9953f217-f020-4680-b62f-2132b7132be0	2018-10-07 08:44:00+00	2018-10-07 09:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	476e62b4-d63a-4060-97a3-626a353c771f	undefined
eb360f8d-a814-40b2-9c0c-5aeb4954f4ea	2018-10-08 08:44:00+00	2018-10-08 09:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	476e62b4-d63a-4060-97a3-626a353c771f	undefined
ad41fa14-3484-4caf-a9d6-e31b8c806aaa	2018-10-09 08:44:00+00	2018-10-09 09:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	476e62b4-d63a-4060-97a3-626a353c771f	undefined
505c4676-edeb-4b61-b936-03012b2558d8	2018-10-10 08:44:00+00	2018-10-10 09:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	476e62b4-d63a-4060-97a3-626a353c771f	undefined
a25e892c-3060-4ee5-886d-0778bb86772f	2018-10-11 08:44:00+00	2018-10-11 09:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	476e62b4-d63a-4060-97a3-626a353c771f	undefined
22c8b884-45e2-48c4-a1b7-b891e1647124	2018-10-12 08:44:00+00	2018-10-12 09:00:00+00	fdb25787-150f-4117-a757-b1cd399b98f3	476e62b4-d63a-4060-97a3-626a353c771f	undefined
5e96463b-b029-4d5f-81e2-2b7b5396ff45	2018-10-16 10:41:00+00	2018-10-16 00:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
85ae56ea-dcd3-42b7-986c-bbaff0f9b67a	2018-10-23 10:41:00+00	2018-10-23 00:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
f8893958-6386-4426-bbb9-7dc525fdab74	2018-10-30 10:41:00+00	2018-10-30 00:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
2d7bb9e1-8ecb-4496-acd6-f0534c269d0f	2018-11-06 10:41:00+00	2018-11-06 00:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
f9b79edd-05c5-4348-8ecc-ea918cca262e	2018-11-13 10:41:00+00	2018-11-13 00:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
154b9c93-3dde-46ab-b299-44abe9971edc	2018-11-20 10:41:00+00	2018-11-20 00:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
0cea2829-612f-419e-bad2-58dfa71b1faf	2018-11-27 10:41:00+00	2018-11-27 00:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
95f52ce5-a409-4676-8e63-7c9ca8d63c7a	2018-10-16 08:44:00+00	2018-10-16 09:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	476e62b4-d63a-4060-97a3-626a353c771f	undefined
b1462757-90b5-4c9a-8975-67118e5d7b6c	2018-10-17 08:44:00+00	2018-10-17 09:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	476e62b4-d63a-4060-97a3-626a353c771f	undefined
b22d5daa-ff23-4714-b1ec-08736d0fe072	2018-10-18 08:44:00+00	2018-10-18 09:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	476e62b4-d63a-4060-97a3-626a353c771f	undefined
59e8ca56-945c-4b37-8f6b-7ff575c099fb	2018-10-19 08:44:00+00	2018-10-19 09:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	476e62b4-d63a-4060-97a3-626a353c771f	undefined
6310a915-6f4a-49c1-a7b3-76cf9a2e4f00	2018-10-20 08:44:00+00	2018-10-20 09:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	476e62b4-d63a-4060-97a3-626a353c771f	undefined
06b23dde-e3aa-47bf-846e-e78cfe4fc5df	2018-10-21 08:44:00+00	2018-10-21 09:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	476e62b4-d63a-4060-97a3-626a353c771f	undefined
5490a590-5b19-4b29-ac35-9e23c3539c17	2018-10-22 08:44:00+00	2018-10-22 09:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	476e62b4-d63a-4060-97a3-626a353c771f	undefined
10af2fd4-b607-4bc0-9bf6-1803d54d0714	2018-10-23 08:44:00+00	2018-10-23 09:00:00+00	a52bdf43-4e23-4d89-a931-cb36e6979a12	476e62b4-d63a-4060-97a3-626a353c771f	undefined
de568f1e-20ae-424a-b5a2-2a72d4a3c8f5	2018-10-17 10:41:00+00	2018-10-17 00:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
ac91ba14-36c5-41ea-93d7-2bd6265c0c9a	2018-10-24 10:41:00+00	2018-10-24 00:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
97d9e5e9-315c-44df-bf01-18bd62e88415	2018-10-31 10:41:00+00	2018-10-31 00:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
2da0bdd9-24e8-4338-84a0-6a17cb529bb7	2018-11-07 10:41:00+00	2018-11-07 00:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
0d2721c3-5761-452d-9389-e669868e7f2b	2018-11-14 10:41:00+00	2018-11-14 00:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
10d94d19-db80-42d3-974c-d6eef5c2a879	2018-11-21 10:41:00+00	2018-11-21 00:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
d91a69a5-d8a3-43a6-9505-c46779786321	2018-11-28 10:41:00+00	2018-11-28 00:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	68475d2d-52e3-4376-9945-b70e3ad29dad	undefined
f54a8b89-cbdd-47dd-b897-e515094f9027	2018-10-17 08:44:00+00	2018-10-17 09:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	476e62b4-d63a-4060-97a3-626a353c771f	undefined
af33af43-6a5f-49d7-9a1f-8f01de66eca8	2018-10-18 08:44:00+00	2018-10-18 09:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	476e62b4-d63a-4060-97a3-626a353c771f	undefined
31c0c7f7-ba85-4df2-9924-0ee729b78770	2018-10-19 08:44:00+00	2018-10-19 09:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	476e62b4-d63a-4060-97a3-626a353c771f	undefined
cced7361-2bcc-4c51-8ae5-8e123b1692c2	2018-10-20 08:44:00+00	2018-10-20 09:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	476e62b4-d63a-4060-97a3-626a353c771f	undefined
ff2f43fb-ca6b-4217-b286-d4485032989e	2018-10-21 08:44:00+00	2018-10-21 09:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	476e62b4-d63a-4060-97a3-626a353c771f	undefined
dc09316b-1555-4b62-8072-384f306fbfb2	2018-10-22 08:44:00+00	2018-10-22 09:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	476e62b4-d63a-4060-97a3-626a353c771f	undefined
c2cd3c92-d56a-462d-906e-5eeeda34bf2e	2018-10-23 08:44:00+00	2018-10-23 09:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	476e62b4-d63a-4060-97a3-626a353c771f	undefined
0417ab3e-4b6c-4b6f-b827-c792c2fb708d	2018-10-24 08:44:00+00	2018-10-24 09:00:00+00	c222e159-26f4-4bd6-9ea5-863f0cb0df71	476e62b4-d63a-4060-97a3-626a353c771f	undefined
\.


--
-- Data for Name: tasks_teamtasktemplate; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_teamtasktemplate (id, start_on_day, frequency, repeat_amount, appear_time, due_time, name, is_manager_task, category, plan_template_id, role_id) FROM stdin;
68475d2d-52e3-4376-9945-b70e3ad29dad	0	weekly	-1	10:41:00	00:00:00	SOmething	f	interaction	719563fb-6394-47b8-89e0-3f6f4fad9c9f	\N
476e62b4-d63a-4060-97a3-626a353c771f	0	daily	8	08:44:00	09:00:00	Test Task	f	interaction	719563fb-6394-47b8-89e0-3f6f4fad9c9f	\N
\.


--
-- Data for Name: tasks_vitalquestion; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_vitalquestion (id, prompt, answer_type, vital_task_template_id) FROM stdin;
2cd8047f-2425-4fa6-a983-09a2784594e6	What time did you go to bed?	time	6b6df74f-1f39-44ef-8555-81f0a9aa8923
707d09a9-d7ec-4b92-aeff-120b3036950c	What time did you get up?	time	6b6df74f-1f39-44ef-8555-81f0a9aa8923
875ae890-b337-4bfd-a698-54ac5d879513	How did you feel when you got up?	scale	6b6df74f-1f39-44ef-8555-81f0a9aa8923
425ad8a2-f65a-41cb-85df-16608477ab2d	Rate the quality of your sleep	scale	6b6df74f-1f39-44ef-8555-81f0a9aa8923
0f767f65-20e7-4ef0-8af9-068208dc0648	How was your energy?	scale	6b6df74f-1f39-44ef-8555-81f0a9aa8923
d5deab18-8084-4cd1-b38e-88c3f9d20426	How many trips to the bathroom?	integer	6b6df74f-1f39-44ef-8555-81f0a9aa8923
e84a3496-b2ad-4518-acc6-14113eec3797	How many trips to the bathroom?	integer	6b6df74f-1f39-44ef-8555-81f0a9aa8923
f26e0c6e-25ab-4322-a099-0ed86f73ecd2	What was the weather like last night?	string	6b6df74f-1f39-44ef-8555-81f0a9aa8923
87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	What is the difference between -1 and 1?	float	6b6df74f-1f39-44ef-8555-81f0a9aa8923
\.


--
-- Data for Name: tasks_vitalresponse; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_vitalresponse (id, answer_boolean, answer_time, answer_float, answer_integer, answer_scale, answer_string, question_id, vital_task_id) FROM stdin;
d9bcd45a-cdd9-4bbc-81ad-c971b0b8e98b	\N	\N	2.10000000000000009	\N	\N		87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	85fc0819-46e0-4806-92d7-7e0cb3f7612e
2172da9d-e58f-42fe-81c6-359ddc0c820e	\N	\N	\N	\N	\N	2.1	f26e0c6e-25ab-4322-a099-0ed86f73ecd2	85fc0819-46e0-4806-92d7-7e0cb3f7612e
073719e9-eb7c-4c0c-8337-14f9df038131	\N	\N	2.10000000000000009	\N	\N		87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	85fc0819-46e0-4806-92d7-7e0cb3f7612e
99ccb364-7edf-4a12-bc9c-c77517df16c7	\N	\N	\N	\N	\N	stormy	f26e0c6e-25ab-4322-a099-0ed86f73ecd2	85fc0819-46e0-4806-92d7-7e0cb3f7612e
388baca4-d21e-4de5-8346-bf5478eeaaf3	\N	\N	2.10000000000000009	\N	\N		87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	85fc0819-46e0-4806-92d7-7e0cb3f7612e
23e41ec0-6307-49cd-8b39-d0606318e0c2	\N	\N	\N	\N	\N	stormy	f26e0c6e-25ab-4322-a099-0ed86f73ecd2	85fc0819-46e0-4806-92d7-7e0cb3f7612e
02270f1f-fa2b-420f-8c79-f012ee7dde4a	\N	\N	0	\N	\N		87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	868b3699-c731-44f2-a726-c5dfd46aa938
7ee3a185-6975-4f43-914f-96f5be370006	\N	\N	\N	\N	\N	stormy	f26e0c6e-25ab-4322-a099-0ed86f73ecd2	868b3699-c731-44f2-a726-c5dfd46aa938
cb568dbf-a7f5-4e2f-97ad-39fc0f2a99ad	\N	\N	\N	0	\N		e84a3496-b2ad-4518-acc6-14113eec3797	868b3699-c731-44f2-a726-c5dfd46aa938
df345fcf-5df9-4508-aef6-5c9b1fe4c29b	\N	\N	\N	0	\N		d5deab18-8084-4cd1-b38e-88c3f9d20426	868b3699-c731-44f2-a726-c5dfd46aa938
332efe94-d79d-444f-bfe3-6b90af5b1fd1	\N	\N	\N	\N	4		0f767f65-20e7-4ef0-8af9-068208dc0648	868b3699-c731-44f2-a726-c5dfd46aa938
cd117e80-4b38-4c27-9951-81d9ddbc6d52	\N	\N	\N	\N	4		425ad8a2-f65a-41cb-85df-16608477ab2d	868b3699-c731-44f2-a726-c5dfd46aa938
e1b25e35-e5e0-4688-8d70-9703da08e032	\N	\N	\N	\N	4		875ae890-b337-4bfd-a698-54ac5d879513	868b3699-c731-44f2-a726-c5dfd46aa938
e8161ad0-4be9-4455-b75a-2655dc3db977	\N	06:00:00	\N	\N	\N		707d09a9-d7ec-4b92-aeff-120b3036950c	868b3699-c731-44f2-a726-c5dfd46aa938
6e4525f6-1fb4-43db-a916-dffcd482ee55	\N	22:00:00	\N	\N	\N		2cd8047f-2425-4fa6-a983-09a2784594e6	868b3699-c731-44f2-a726-c5dfd46aa938
b5b2fe91-e6f9-41c8-9d53-c085468947e9	\N	\N	0	\N	\N		87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	868b3699-c731-44f2-a726-c5dfd46aa938
5e2c9842-0d6a-40fa-aa32-eb41e6e4d69a	\N	\N	\N	\N	\N	ttt	f26e0c6e-25ab-4322-a099-0ed86f73ecd2	868b3699-c731-44f2-a726-c5dfd46aa938
32dfc786-9d4a-4539-9c08-6accf5015acc	\N	\N	\N	0	\N		e84a3496-b2ad-4518-acc6-14113eec3797	868b3699-c731-44f2-a726-c5dfd46aa938
1d17c203-c69d-4dd0-a3a1-cf3e4a805961	\N	\N	\N	0	\N		d5deab18-8084-4cd1-b38e-88c3f9d20426	868b3699-c731-44f2-a726-c5dfd46aa938
d80cfa48-9a6e-4db9-8033-490f627dc9a5	\N	\N	\N	\N	4		0f767f65-20e7-4ef0-8af9-068208dc0648	868b3699-c731-44f2-a726-c5dfd46aa938
625f701a-2ac3-4bd3-8aa6-396b8189b9b2	\N	\N	\N	\N	4		425ad8a2-f65a-41cb-85df-16608477ab2d	868b3699-c731-44f2-a726-c5dfd46aa938
a8cebccd-a342-4cc1-b4df-e8f12fd687da	\N	\N	\N	\N	4		875ae890-b337-4bfd-a698-54ac5d879513	868b3699-c731-44f2-a726-c5dfd46aa938
b0ac2422-9222-4123-8728-1f91a774402a	\N	00:00:00	\N	\N	\N		707d09a9-d7ec-4b92-aeff-120b3036950c	868b3699-c731-44f2-a726-c5dfd46aa938
f36b26bc-fb01-4cf6-906e-ac59dbc62853	\N	00:00:00	\N	\N	\N		2cd8047f-2425-4fa6-a983-09a2784594e6	868b3699-c731-44f2-a726-c5dfd46aa938
2b84fde6-5f2f-4a31-a753-17eac00a345e	\N	\N	0	\N	\N		87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	868b3699-c731-44f2-a726-c5dfd46aa938
e58ac2f7-bcf3-4a7e-988f-d861389bd4a2	\N	\N	\N	\N	\N	gghjj	f26e0c6e-25ab-4322-a099-0ed86f73ecd2	868b3699-c731-44f2-a726-c5dfd46aa938
f5d2ec93-3382-4ce8-8978-ec193f228dd2	\N	\N	\N	0	\N		e84a3496-b2ad-4518-acc6-14113eec3797	868b3699-c731-44f2-a726-c5dfd46aa938
7062e61e-c28c-422b-93c0-2d14d1f045b6	\N	\N	\N	0	\N		d5deab18-8084-4cd1-b38e-88c3f9d20426	868b3699-c731-44f2-a726-c5dfd46aa938
10df5f23-89bf-48f9-9658-d0e1d54e4162	\N	\N	\N	\N	4		0f767f65-20e7-4ef0-8af9-068208dc0648	868b3699-c731-44f2-a726-c5dfd46aa938
4ccd6bbe-c6c2-49ca-a384-b3e7db074f3a	\N	\N	\N	\N	4		425ad8a2-f65a-41cb-85df-16608477ab2d	868b3699-c731-44f2-a726-c5dfd46aa938
f93e4ff9-12cd-4f0f-85da-8f04ec222cb5	\N	\N	\N	\N	4		875ae890-b337-4bfd-a698-54ac5d879513	868b3699-c731-44f2-a726-c5dfd46aa938
6d60924a-27a4-49c5-b24b-2950bc53a04f	\N	00:00:00	\N	\N	\N		707d09a9-d7ec-4b92-aeff-120b3036950c	868b3699-c731-44f2-a726-c5dfd46aa938
aab5691b-ef12-43b5-af03-97d3ebd763d7	\N	00:00:00	\N	\N	\N		2cd8047f-2425-4fa6-a983-09a2784594e6	868b3699-c731-44f2-a726-c5dfd46aa938
440a620a-e7d4-4af7-a65f-c22c36e7dada	\N	\N	0	\N	\N		87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	868b3699-c731-44f2-a726-c5dfd46aa938
4ed532b6-997a-432f-bbeb-afb7bba8ffb7	\N	\N	\N	\N	\N	ttjgg	f26e0c6e-25ab-4322-a099-0ed86f73ecd2	868b3699-c731-44f2-a726-c5dfd46aa938
2225a4d3-6ffd-469f-920e-52992e2ae250	\N	\N	\N	0	\N		e84a3496-b2ad-4518-acc6-14113eec3797	868b3699-c731-44f2-a726-c5dfd46aa938
1e4ed4d9-9970-402d-8e9d-24751dbbeb54	\N	\N	\N	0	\N		d5deab18-8084-4cd1-b38e-88c3f9d20426	868b3699-c731-44f2-a726-c5dfd46aa938
88e452e8-f89f-480f-95f0-2a1af7e428d6	\N	\N	\N	\N	4		0f767f65-20e7-4ef0-8af9-068208dc0648	868b3699-c731-44f2-a726-c5dfd46aa938
7f07bc7a-5dcc-456c-a07b-9c6b9b371ab9	\N	\N	\N	\N	4		425ad8a2-f65a-41cb-85df-16608477ab2d	868b3699-c731-44f2-a726-c5dfd46aa938
51465d9e-6403-421d-8827-979da99878c1	\N	\N	\N	\N	4		875ae890-b337-4bfd-a698-54ac5d879513	868b3699-c731-44f2-a726-c5dfd46aa938
eca02f76-4ad7-42cf-83a5-dcc38dc75df5	\N	00:00:00	\N	\N	\N		707d09a9-d7ec-4b92-aeff-120b3036950c	868b3699-c731-44f2-a726-c5dfd46aa938
cdd41b61-7b65-4009-ae2d-b44a70840ac4	\N	00:00:00	\N	\N	\N		2cd8047f-2425-4fa6-a983-09a2784594e6	868b3699-c731-44f2-a726-c5dfd46aa938
8289147e-439b-4693-a13c-3c33ab7c2b06	\N	\N	0	\N	\N		87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	868b3699-c731-44f2-a726-c5dfd46aa938
18b263e5-cf6f-44f1-bb92-0a4f2aa5714a	\N	\N	\N	\N	\N	ttjg	f26e0c6e-25ab-4322-a099-0ed86f73ecd2	868b3699-c731-44f2-a726-c5dfd46aa938
bb168c1a-9bbf-45f5-bb19-7094e0b3e965	\N	\N	\N	0	\N		e84a3496-b2ad-4518-acc6-14113eec3797	868b3699-c731-44f2-a726-c5dfd46aa938
30cfa87f-c323-4e47-b4cf-0ad68871ae59	\N	\N	\N	0	\N		d5deab18-8084-4cd1-b38e-88c3f9d20426	868b3699-c731-44f2-a726-c5dfd46aa938
69b12cdf-b3cd-44e3-bcd7-53e87729502b	\N	\N	\N	\N	4		0f767f65-20e7-4ef0-8af9-068208dc0648	868b3699-c731-44f2-a726-c5dfd46aa938
d8a146ac-2d58-493b-b79f-1a5bc620630f	\N	\N	\N	\N	4		425ad8a2-f65a-41cb-85df-16608477ab2d	868b3699-c731-44f2-a726-c5dfd46aa938
a8359983-79a1-4902-9f89-74eaf0f78d11	\N	\N	\N	\N	4		875ae890-b337-4bfd-a698-54ac5d879513	868b3699-c731-44f2-a726-c5dfd46aa938
bda088a7-4a91-44cd-a1e3-49c55ac0e5d8	\N	00:00:00	\N	\N	\N		707d09a9-d7ec-4b92-aeff-120b3036950c	868b3699-c731-44f2-a726-c5dfd46aa938
29e39b75-f607-40e1-9762-b9d6f736897c	\N	00:00:00	\N	\N	\N		2cd8047f-2425-4fa6-a983-09a2784594e6	868b3699-c731-44f2-a726-c5dfd46aa938
dda234ed-b9b8-4d0b-958d-836d0f714b9f	\N	\N	2	\N	\N		87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	868b3699-c731-44f2-a726-c5dfd46aa938
ed9c7be4-aadc-4e93-9adf-231d39b9fe9b	\N	\N	\N	\N	\N	hbcgh	f26e0c6e-25ab-4322-a099-0ed86f73ecd2	868b3699-c731-44f2-a726-c5dfd46aa938
70e6df80-54ef-4bda-9f30-dd53396c9d88	\N	\N	\N	10	\N		e84a3496-b2ad-4518-acc6-14113eec3797	868b3699-c731-44f2-a726-c5dfd46aa938
d12bf5ba-0834-4a0b-ad68-662cadc69ded	\N	\N	\N	1	\N		d5deab18-8084-4cd1-b38e-88c3f9d20426	868b3699-c731-44f2-a726-c5dfd46aa938
e3764347-d9f1-4a14-a642-b5c14b90bdae	\N	\N	\N	\N	4		0f767f65-20e7-4ef0-8af9-068208dc0648	868b3699-c731-44f2-a726-c5dfd46aa938
5e889ac5-6859-4eb2-a613-93e7199b2326	\N	\N	\N	\N	4		425ad8a2-f65a-41cb-85df-16608477ab2d	868b3699-c731-44f2-a726-c5dfd46aa938
6b792f47-315b-440f-b1fe-2fae2d62ccf5	\N	\N	\N	\N	4		875ae890-b337-4bfd-a698-54ac5d879513	868b3699-c731-44f2-a726-c5dfd46aa938
d27e133b-ebca-4441-816a-b9e844eae35f	\N	06:00:00	\N	\N	\N		707d09a9-d7ec-4b92-aeff-120b3036950c	868b3699-c731-44f2-a726-c5dfd46aa938
0ba5f07e-b49a-47f0-9bf9-e9ca68ff4de5	\N	22:00:00	\N	\N	\N		2cd8047f-2425-4fa6-a983-09a2784594e6	868b3699-c731-44f2-a726-c5dfd46aa938
a7f35a88-a7bf-48b5-ab1b-75b5c3c3cae5	\N	13:52:11	\N	\N	\N		2cd8047f-2425-4fa6-a983-09a2784594e6	b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb
0f7c4fb4-8d37-45be-b701-e1510af8d931	\N	13:52:12	\N	\N	\N		707d09a9-d7ec-4b92-aeff-120b3036950c	b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb
eed0e94b-024a-4285-b5a6-bcedcfb173c4	\N	\N	\N	\N	\N	Good	875ae890-b337-4bfd-a698-54ac5d879513	b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb
861b1a2a-c1f7-420b-a492-49124f0790ed	\N	\N	\N	\N	5		425ad8a2-f65a-41cb-85df-16608477ab2d	b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb
7cb4c32d-8ec7-4e1c-b4b7-aac520d76ae4	\N	\N	\N	\N	5		0f767f65-20e7-4ef0-8af9-068208dc0648	b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb
0efacc73-a66a-46d2-bf7f-65fe93f35464	\N	\N	\N	1	\N		d5deab18-8084-4cd1-b38e-88c3f9d20426	b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb
83dc31c1-d0a6-4f55-a4f4-a96b6393599b	\N	\N	\N	1	\N		e84a3496-b2ad-4518-acc6-14113eec3797	b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb
9f100506-4484-495a-9525-65cd74031b0b	\N	\N	\N	\N	\N	Good	f26e0c6e-25ab-4322-a099-0ed86f73ecd2	b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb
b1390c96-6236-4e8c-a0e5-18838fabf5d8	\N	\N	1	\N	\N		87f38ce3-e2a5-4f93-87fa-ed08d33cde0d	b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb
\.


--
-- Data for Name: tasks_vitaltask; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_vitaltask (id, appear_datetime, due_datetime, is_complete, plan_id, vital_task_template_id) FROM stdin;
e5b2312c-16d5-48a5-bd04-2203c35cd885	2018-10-05 01:00:00+00	2018-10-05 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
82ac6405-350e-408a-bb2c-dc7fa6aa59fc	2018-10-06 01:00:00+00	2018-10-06 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
fe7fa4f2-0cfd-4f43-b428-eeecbe4f2845	2018-10-07 01:00:00+00	2018-10-07 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
29ef4ea1-334b-48b7-953b-d232d4f2823e	2018-10-08 01:00:00+00	2018-10-08 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
85fc0819-46e0-4806-92d7-7e0cb3f7612e	2018-10-09 01:00:00+00	2018-10-09 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
d8931a64-e114-4e1b-be47-f20b80a2a517	2018-10-16 01:00:00+00	2018-10-16 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
65a8574c-3557-4e0e-a841-443d1004dec1	2018-10-11 01:00:00+00	2018-10-11 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
b5fa9861-e2f2-4489-a7a7-10c97488a3de	2018-10-12 01:00:00+00	2018-10-12 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
e5a2111d-d48c-4ba1-ad09-8e66db695e38	2018-10-13 01:00:00+00	2018-10-13 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
7bf3d840-bd14-4cd6-96da-2c3916db2da5	2018-10-14 01:00:00+00	2018-10-14 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
c5b4a46b-2024-4da4-a982-c4c24eadacb6	2018-10-15 01:00:00+00	2018-10-15 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
aca14822-1fd0-47a2-b04c-763cc6b82b2d	2018-10-16 01:00:00+00	2018-10-16 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
a6aa6727-be7d-46dc-b8f9-dcb45572ee92	2018-10-17 01:00:00+00	2018-10-17 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
424dcf62-5629-4858-845c-9e1e224826f6	2018-10-18 01:00:00+00	2018-10-18 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
712382be-613e-4178-9864-431e4aedc02d	2018-10-19 01:00:00+00	2018-10-19 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
62b4ed45-db29-404b-953b-0e6a2f06e084	2018-10-20 01:00:00+00	2018-10-20 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
ca02b634-f5fc-49a8-adf2-679beeb23838	2018-10-21 01:00:00+00	2018-10-21 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
272d7a48-a873-4c25-b244-8a9e8472c217	2018-10-22 01:00:00+00	2018-10-22 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
8370d998-733f-4416-80aa-9eaa7541488c	2018-10-23 01:00:00+00	2018-10-23 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
87df904a-89a4-4f3d-9e4e-79a2c1a4bdd6	2018-10-24 01:00:00+00	2018-10-24 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
87c66ad4-9976-421d-ab3f-0388dd04d9b4	2018-10-25 01:00:00+00	2018-10-25 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
202856b7-8349-4f2d-bd12-65e722ce4a5e	2018-10-26 01:00:00+00	2018-10-26 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
e79c8272-7e82-478b-a201-cf88333a25e6	2018-10-27 01:00:00+00	2018-10-27 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
f57faf68-f9de-42de-aaba-73c8f91054d7	2018-10-28 01:00:00+00	2018-10-28 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
8982acd7-5e40-4be1-b8b1-c0801913a9df	2018-10-29 01:00:00+00	2018-10-29 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
2eade8f5-e48f-47c3-a27e-86855bc41d9a	2018-10-30 01:00:00+00	2018-10-30 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
a415313b-156f-4bb6-8373-fb75d6b0e570	2018-10-31 01:00:00+00	2018-10-31 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
0d6e971a-837e-4d7f-a9bf-9771b06a23df	2018-11-01 01:00:00+00	2018-11-01 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
d3e5ea97-4b17-4d48-ace0-7b526057fd49	2018-11-02 01:00:00+00	2018-11-02 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
37e62380-d420-44b4-aed1-288706d84e93	2018-11-03 01:00:00+00	2018-11-03 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
8f128ff4-80a8-40b0-9d7e-b8dcc84c0f17	2018-11-04 01:00:00+00	2018-11-04 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
1aeb2fe7-1a07-4b30-a238-e894d7900119	2018-11-05 01:00:00+00	2018-11-05 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
29689249-b427-47e9-bae5-bb797ac61f6f	2018-11-06 01:00:00+00	2018-11-06 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
38c6571e-7b62-4066-8a10-8c0778e2734f	2018-11-07 01:00:00+00	2018-11-07 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
b49fce65-8f73-49e2-86ab-087a510525c5	2018-11-08 01:00:00+00	2018-11-08 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
e2b51c9f-3891-43ea-bfb9-ea86bd31e4ca	2018-11-09 01:00:00+00	2018-11-09 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
c8cee2c9-8660-43e2-9807-9a9b821cfa1f	2018-11-10 01:00:00+00	2018-11-10 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
67d56958-7e5c-46d8-89d1-60a7cdfe15fb	2018-11-11 01:00:00+00	2018-11-11 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
19e09311-624c-4d7c-89a6-c3c74eb84b18	2018-11-12 01:00:00+00	2018-11-12 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
2d10ff94-4960-4af9-8458-1a8f6d8dee97	2018-11-13 01:00:00+00	2018-11-13 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
bae3cd8c-3010-431e-a113-197f7e15ff63	2018-11-14 01:00:00+00	2018-11-14 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
055b67c7-8a1b-4581-82b8-53e777982b62	2018-11-15 01:00:00+00	2018-11-15 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
31a6d97e-1cc5-4347-8497-6a9eba73ab23	2018-11-16 01:00:00+00	2018-11-16 15:03:00+00	f	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
114744cb-dd3c-478f-a798-f02c4986daac	2018-10-17 01:00:00+00	2018-10-17 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
ca608d94-e7f0-41d4-a8e6-504c51fd2b15	2018-10-18 01:00:00+00	2018-10-18 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
b37124c7-c476-4821-82c2-d0fc9395a043	2018-10-19 01:00:00+00	2018-10-19 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
6f8e92b9-e234-4199-8dd9-502b94215844	2018-10-20 01:00:00+00	2018-10-20 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
a468a1e3-5db9-48c6-a4b0-cef75fce5621	2018-10-21 01:00:00+00	2018-10-21 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
9a8e8562-2ddb-4483-a015-3fb318fbc8d2	2018-10-22 01:00:00+00	2018-10-22 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
f9a71f92-68c7-425d-ad5e-dd7e1c2b9796	2018-10-23 01:00:00+00	2018-10-23 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
4171b94a-5ac6-4367-8d39-59c048231772	2018-10-25 01:00:00+00	2018-10-25 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
ede9c880-c238-4ec2-90ac-e8f309cb4796	2018-10-26 01:00:00+00	2018-10-26 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
11691c1a-4538-4688-9b8a-89662b4587ba	2018-10-27 01:00:00+00	2018-10-27 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
121ba085-acbb-4f1d-a80e-600743b9daba	2018-10-28 01:00:00+00	2018-10-28 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
b8a0b680-f708-46ea-8720-809d086307fe	2018-10-29 01:00:00+00	2018-10-29 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
511ffefd-ffb3-48d7-a2f3-4ceebc03bb43	2018-10-30 01:00:00+00	2018-10-30 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
1680f3a9-dd83-4225-b305-d5849b849392	2018-10-31 01:00:00+00	2018-10-31 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
ceec12fb-70d5-43a9-90b0-ebbef37bc6cf	2018-11-01 01:00:00+00	2018-11-01 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
c2c4c228-4389-49bf-9469-f8e3898c0f28	2018-11-02 01:00:00+00	2018-11-02 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
edee9e9d-f33d-4dfc-a0ca-41b3770375aa	2018-11-03 01:00:00+00	2018-11-03 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
81718d27-5b4d-4d03-b2ac-52e29c6bd2a6	2018-11-04 01:00:00+00	2018-11-04 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
fbdf1122-4e44-4184-8245-ac3dc88552ed	2018-11-05 01:00:00+00	2018-11-05 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
4e97ea21-63ad-459f-b86d-a86d3db51be6	2018-11-06 01:00:00+00	2018-11-06 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
b1b7c75b-855e-4479-9535-8e8cd0fa7453	2018-11-07 01:00:00+00	2018-11-07 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
a4f7674d-e6e2-49ab-aecc-c61ff8307511	2018-11-08 01:00:00+00	2018-11-08 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
d4ab3363-0bd6-4248-a0b9-c5fa19279d35	2018-11-09 01:00:00+00	2018-11-09 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
e19b518f-0b66-410c-9685-ac6c9455e164	2018-11-10 01:00:00+00	2018-11-10 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
3149db41-42a9-4607-8670-198e97ef17a1	2018-11-11 01:00:00+00	2018-11-11 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
13907ade-7872-40df-92b5-8d8c603bb8ed	2018-11-12 01:00:00+00	2018-11-12 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
3660ed25-ce4a-4654-9b7c-b12273622815	2018-11-13 01:00:00+00	2018-11-13 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
fa8c6def-51f7-42c5-bbfe-ef0bf222e7e8	2018-11-14 01:00:00+00	2018-11-14 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
3da7fe74-b7be-41cc-af15-fee66b4f34e3	2018-11-15 01:00:00+00	2018-11-15 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
48c50764-7a93-4d36-8457-531b9af528e4	2018-11-16 01:00:00+00	2018-11-16 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
3df9417c-e3aa-4a70-9c5b-c0fe997e57f5	2018-11-17 01:00:00+00	2018-11-17 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
85f7552d-9a5d-465d-8d64-2b48123c66ee	2018-11-18 01:00:00+00	2018-11-18 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
124655a1-34aa-4045-ba1e-bb6859cfdbb4	2018-11-19 01:00:00+00	2018-11-19 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
31712fa9-d6e3-4d26-9b06-96d7e6e3d7e5	2018-11-20 01:00:00+00	2018-11-20 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
8e488ec7-7db3-4db9-9d0f-996933f74012	2018-11-21 01:00:00+00	2018-11-21 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
455254f9-b1a4-40b2-9c8c-b8140252a093	2018-11-22 01:00:00+00	2018-11-22 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
5c1229d2-8cc8-4303-bd53-08bae74cbd76	2018-11-23 01:00:00+00	2018-11-23 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
541b1ec0-21bf-44ee-a65b-f818255336ee	2018-11-24 01:00:00+00	2018-11-24 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
7d1c0ecc-8e52-418b-bdbf-ea7ba972418f	2018-11-25 01:00:00+00	2018-11-25 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
59831d17-2e5b-4617-8f46-530a945579ef	2018-11-26 01:00:00+00	2018-11-26 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
7d861fbe-fd6b-4d72-b762-7c5c5fe1af10	2018-11-27 01:00:00+00	2018-11-27 15:03:00+00	f	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
868b3699-c731-44f2-a726-c5dfd46aa938	2018-10-10 01:00:00+00	2018-10-10 15:03:00+00	t	fdb25787-150f-4117-a757-b1cd399b98f3	6b6df74f-1f39-44ef-8555-81f0a9aa8923
5cad3ec5-4abd-4403-8bcf-f654e93034ad	2018-10-17 01:00:00+00	2018-10-17 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
aac5f319-5a3a-49b3-91f9-41afa12f428e	2018-10-18 01:00:00+00	2018-10-18 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
6cc4e179-511c-458b-a5ca-ed2206b027cb	2018-10-19 01:00:00+00	2018-10-19 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
4c1911a0-7b3a-4706-9c87-39f34fd0b766	2018-10-20 01:00:00+00	2018-10-20 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
dace69fa-0089-4f8c-b3b3-036b02aefc6e	2018-10-21 01:00:00+00	2018-10-21 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
4c114a22-dea6-4c2d-a8ad-7fcaa5a075f0	2018-10-22 01:00:00+00	2018-10-22 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
50a6c24c-784e-4e8f-a958-8b1c50cb6768	2018-10-23 01:00:00+00	2018-10-23 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
f68fdde7-5cdc-4747-be19-01c41dbd4334	2018-10-24 01:00:00+00	2018-10-24 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
cc8103dd-29a0-4827-a057-32c926d98eec	2018-10-25 01:00:00+00	2018-10-25 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
c7bb11be-2fa5-434e-88a4-740c92c5e1f3	2018-10-26 01:00:00+00	2018-10-26 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
ffc8c4f2-cc5b-467d-bcff-2271392b770d	2018-10-27 01:00:00+00	2018-10-27 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
cabad46a-89ad-4410-a870-df7e3c912d65	2018-10-28 01:00:00+00	2018-10-28 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
269908b6-247b-4654-8d13-7a715177ba28	2018-10-29 01:00:00+00	2018-10-29 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
257debfd-b2b3-4884-a41a-b0900b996628	2018-10-30 01:00:00+00	2018-10-30 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
0657e49e-11e5-4edb-96e1-ceb29b8fc384	2018-10-31 01:00:00+00	2018-10-31 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
2aa05621-f9dc-4b99-84e5-2bb79444960b	2018-11-01 01:00:00+00	2018-11-01 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
1901585c-0eae-436d-a3d1-774418e42324	2018-11-02 01:00:00+00	2018-11-02 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
9685a5af-e47c-4a9f-a967-73df4bb590d0	2018-11-03 01:00:00+00	2018-11-03 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
61eb43f8-b5c7-49b2-8f94-ea4b635b83cd	2018-11-04 01:00:00+00	2018-11-04 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
3ea71fc4-6628-4fcc-9160-fb8b00c3a609	2018-11-05 01:00:00+00	2018-11-05 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
0eca1865-c18e-45f4-a03c-322bc2e3a51a	2018-11-06 01:00:00+00	2018-11-06 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
6ca5f813-6082-447f-84f8-de184d6e38b1	2018-11-07 01:00:00+00	2018-11-07 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
f9183196-6180-4a99-9719-377ad920dacb	2018-11-08 01:00:00+00	2018-11-08 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
2889a84e-f9da-4580-be47-86c6d4c3dad5	2018-11-09 01:00:00+00	2018-11-09 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
476e8fb6-622c-4c75-a4a2-a770f19f9c8b	2018-11-10 01:00:00+00	2018-11-10 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
a218660e-31b5-471a-bf9d-be0d8db757c3	2018-11-11 01:00:00+00	2018-11-11 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
f40d15ac-4173-46c6-b4a0-1a075e6651af	2018-11-12 01:00:00+00	2018-11-12 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
e079f77d-93df-4ced-a86a-0c476dbbff73	2018-11-13 01:00:00+00	2018-11-13 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
73745798-3f49-448c-8f5e-f272eba4dbd5	2018-11-14 01:00:00+00	2018-11-14 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
a46e0fa1-ca09-4022-a874-aad187eba415	2018-11-15 01:00:00+00	2018-11-15 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
481f2db9-b0d3-420f-be72-6a88b741c9d6	2018-11-16 01:00:00+00	2018-11-16 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
482bff7d-2e03-4caf-af05-69187c3afae2	2018-11-17 01:00:00+00	2018-11-17 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
446e3edf-2e58-4471-94a2-1b351ab45921	2018-11-18 01:00:00+00	2018-11-18 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
5202d646-6c05-4959-925d-b826e1fa7abe	2018-11-19 01:00:00+00	2018-11-19 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
91705129-e63b-4e6d-a0ef-6b4d33e1215b	2018-11-20 01:00:00+00	2018-11-20 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
133269ac-9c33-4865-88fc-070b3e717356	2018-11-21 01:00:00+00	2018-11-21 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
75dfad60-ce7d-45bf-87f3-232721b7ac54	2018-11-22 01:00:00+00	2018-11-22 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
ed6b8a1f-bd9c-442c-9e05-97d09dcbc661	2018-11-23 01:00:00+00	2018-11-23 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
59801c97-5de7-44ac-9683-ac631e0e36de	2018-11-24 01:00:00+00	2018-11-24 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
3216e680-7a78-494c-8ce7-55c27910fc68	2018-11-25 01:00:00+00	2018-11-25 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
558aa26f-7250-4aef-b13c-777eb452f76f	2018-11-26 01:00:00+00	2018-11-26 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
6fce9fc2-79f3-4a5b-9f5f-ccd2c89b3675	2018-11-27 01:00:00+00	2018-11-27 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
f4b4e34b-a5ac-4894-9aa0-5cf166a56609	2018-11-28 01:00:00+00	2018-11-28 15:03:00+00	f	c222e159-26f4-4bd6-9ea5-863f0cb0df71	6b6df74f-1f39-44ef-8555-81f0a9aa8923
b3de7fc9-dfb6-49a9-a005-c01ae64ac9fb	2018-10-24 01:00:00+00	2018-10-24 15:03:00+00	t	a52bdf43-4e23-4d89-a931-cb36e6979a12	6b6df74f-1f39-44ef-8555-81f0a9aa8923
\.


--
-- Data for Name: tasks_vitaltasktemplate; Type: TABLE DATA; Schema: public; Owner: care_adopt_backend
--

COPY public.tasks_vitaltasktemplate (id, start_on_day, frequency, repeat_amount, appear_time, due_time, name, plan_template_id) FROM stdin;
6b6df74f-1f39-44ef-8555-81f0a9aa8923	0	daily	-1	01:00:00	15:03:00	Sleep Report	719563fb-6394-47b8-89e0-3f6f4fad9c9f
\.


--
-- Name: account_emailaddress_email_key; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_email_key UNIQUE (email);


--
-- Name: account_emailaddress_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_pkey PRIMARY KEY (id);


--
-- Name: account_emailconfirmation_key_key; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_key_key UNIQUE (key);


--
-- Name: account_emailconfirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_pkey PRIMARY KEY (id);


--
-- Name: accounts_emailuser_email_key; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.accounts_emailuser
    ADD CONSTRAINT accounts_emailuser_email_key UNIQUE (email);


--
-- Name: accounts_emailuser_groups_emailuser_id_group_id_2be11c51_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.accounts_emailuser_groups
    ADD CONSTRAINT accounts_emailuser_groups_emailuser_id_group_id_2be11c51_uniq UNIQUE (emailuser_id, group_id);


--
-- Name: accounts_emailuser_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.accounts_emailuser_groups
    ADD CONSTRAINT accounts_emailuser_groups_pkey PRIMARY KEY (id);


--
-- Name: accounts_emailuser_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.accounts_emailuser
    ADD CONSTRAINT accounts_emailuser_pkey PRIMARY KEY (id);


--
-- Name: accounts_emailuser_user__emailuser_id_permission__ae88a7bb_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.accounts_emailuser_user_permissions
    ADD CONSTRAINT accounts_emailuser_user__emailuser_id_permission__ae88a7bb_uniq UNIQUE (emailuser_id, permission_id);


--
-- Name: accounts_emailuser_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.accounts_emailuser_user_permissions
    ADD CONSTRAINT accounts_emailuser_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: core_diagnosis_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_diagnosis
    ADD CONSTRAINT core_diagnosis_pkey PRIMARY KEY (id);


--
-- Name: core_employeeprofile_fac_employeeprofile_id_facil_96f47b98_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile_facilities
    ADD CONSTRAINT core_employeeprofile_fac_employeeprofile_id_facil_96f47b98_uniq UNIQUE (employeeprofile_id, facility_id);


--
-- Name: core_employeeprofile_fac_employeeprofile_id_facil_c88c7ad3_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile_facilities_managed
    ADD CONSTRAINT core_employeeprofile_fac_employeeprofile_id_facil_c88c7ad3_uniq UNIQUE (employeeprofile_id, facility_id);


--
-- Name: core_employeeprofile_facilities_managed_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile_facilities_managed
    ADD CONSTRAINT core_employeeprofile_facilities_managed_pkey PRIMARY KEY (id);


--
-- Name: core_employeeprofile_facilities_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile_facilities
    ADD CONSTRAINT core_employeeprofile_facilities_pkey PRIMARY KEY (id);


--
-- Name: core_employeeprofile_org_employeeprofile_id_organ_086a0d4d_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile_organizations_managed
    ADD CONSTRAINT core_employeeprofile_org_employeeprofile_id_organ_086a0d4d_uniq UNIQUE (employeeprofile_id, organization_id);


--
-- Name: core_employeeprofile_org_employeeprofile_id_organ_68c424ff_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile_organizations
    ADD CONSTRAINT core_employeeprofile_org_employeeprofile_id_organ_68c424ff_uniq UNIQUE (employeeprofile_id, organization_id);


--
-- Name: core_employeeprofile_organizations_managed_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile_organizations_managed
    ADD CONSTRAINT core_employeeprofile_organizations_managed_pkey PRIMARY KEY (id);


--
-- Name: core_employeeprofile_organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile_organizations
    ADD CONSTRAINT core_employeeprofile_organizations_pkey PRIMARY KEY (id);


--
-- Name: core_employeeprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile
    ADD CONSTRAINT core_employeeprofile_pkey PRIMARY KEY (id);


--
-- Name: core_employeeprofile_rol_employeeprofile_id_provi_56c4683e_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile_roles
    ADD CONSTRAINT core_employeeprofile_rol_employeeprofile_id_provi_56c4683e_uniq UNIQUE (employeeprofile_id, providerrole_id);


--
-- Name: core_employeeprofile_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile_roles
    ADD CONSTRAINT core_employeeprofile_roles_pkey PRIMARY KEY (id);


--
-- Name: core_employeeprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_employeeprofile
    ADD CONSTRAINT core_employeeprofile_user_id_key UNIQUE (user_id);


--
-- Name: core_facility_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_facility
    ADD CONSTRAINT core_facility_pkey PRIMARY KEY (id);


--
-- Name: core_invitedemailtemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_invitedemailtemplate
    ADD CONSTRAINT core_invitedemailtemplate_pkey PRIMARY KEY (id);


--
-- Name: core_medication_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_medication
    ADD CONSTRAINT core_medication_pkey PRIMARY KEY (id);


--
-- Name: core_organization_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_organization
    ADD CONSTRAINT core_organization_pkey PRIMARY KEY (id);


--
-- Name: core_procedure_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_procedure
    ADD CONSTRAINT core_procedure_pkey PRIMARY KEY (id);


--
-- Name: core_providerrole_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_providerrole
    ADD CONSTRAINT core_providerrole_pkey PRIMARY KEY (id);


--
-- Name: core_providerspecialty_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_providerspecialty
    ADD CONSTRAINT core_providerspecialty_pkey PRIMARY KEY (id);


--
-- Name: core_providertitle_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_providertitle
    ADD CONSTRAINT core_providertitle_pkey PRIMARY KEY (id);


--
-- Name: core_symptom_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.core_symptom
    ADD CONSTRAINT core_symptom_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: patients_patientdiagnosis_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_patientdiagnosis
    ADD CONSTRAINT patients_patientdiagnosis_pkey PRIMARY KEY (id);


--
-- Name: patients_patientmedication_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_patientmedication
    ADD CONSTRAINT patients_patientmedication_pkey PRIMARY KEY (id);


--
-- Name: patients_patientprocedure_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_patientprocedure
    ADD CONSTRAINT patients_patientprocedure_pkey PRIMARY KEY (id);


--
-- Name: patients_patientprofile__patientprofile_id_patien_25ce21db_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_patientprofile_diagnosis
    ADD CONSTRAINT patients_patientprofile__patientprofile_id_patien_25ce21db_uniq UNIQUE (patientprofile_id, patientdiagnosis_id);


--
-- Name: patients_patientprofile_diagnosis_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_patientprofile_diagnosis
    ADD CONSTRAINT patients_patientprofile_diagnosis_pkey PRIMARY KEY (id);


--
-- Name: patients_patientprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_patientprofile
    ADD CONSTRAINT patients_patientprofile_pkey PRIMARY KEY (id);


--
-- Name: patients_patientprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_patientprofile
    ADD CONSTRAINT patients_patientprofile_user_id_key UNIQUE (user_id);


--
-- Name: patients_patientverificationcode_patient_id_code_64109fe3_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_patientverificationcode
    ADD CONSTRAINT patients_patientverificationcode_patient_id_code_64109fe3_uniq UNIQUE (patient_id, code);


--
-- Name: patients_patientverificationcode_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_patientverificationcode
    ADD CONSTRAINT patients_patientverificationcode_pkey PRIMARY KEY (id);


--
-- Name: patients_potentialpatien_potentialpatient_id_faci_8091e638_uniq; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_potentialpatient_facility
    ADD CONSTRAINT patients_potentialpatien_potentialpatient_id_faci_8091e638_uniq UNIQUE (potentialpatient_id, facility_id);


--
-- Name: patients_potentialpatient_facility_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_potentialpatient_facility
    ADD CONSTRAINT patients_potentialpatient_facility_pkey PRIMARY KEY (id);


--
-- Name: patients_potentialpatient_patient_profile_id_key; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_potentialpatient
    ADD CONSTRAINT patients_potentialpatient_patient_profile_id_key UNIQUE (patient_profile_id);


--
-- Name: patients_potentialpatient_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_potentialpatient
    ADD CONSTRAINT patients_potentialpatient_pkey PRIMARY KEY (id);


--
-- Name: patients_problemarea_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_problemarea
    ADD CONSTRAINT patients_problemarea_pkey PRIMARY KEY (id);


--
-- Name: patients_reminderemail_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.patients_reminderemail
    ADD CONSTRAINT patients_reminderemail_pkey PRIMARY KEY (id);


--
-- Name: plans_careplaninstance_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.plans_careplan
    ADD CONSTRAINT plans_careplaninstance_pkey PRIMARY KEY (id);


--
-- Name: plans_careplantemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.plans_careplantemplate
    ADD CONSTRAINT plans_careplantemplate_pkey PRIMARY KEY (id);


--
-- Name: plans_careteammember_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.plans_careteammember
    ADD CONSTRAINT plans_careteammember_pkey PRIMARY KEY (id);


--
-- Name: plans_goal_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.plans_goal
    ADD CONSTRAINT plans_goal_pkey PRIMARY KEY (id);


--
-- Name: plans_goalcomment_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.plans_goalcomment
    ADD CONSTRAINT plans_goalcomment_pkey PRIMARY KEY (id);


--
-- Name: plans_goalprogress_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.plans_goalprogress
    ADD CONSTRAINT plans_goalprogress_pkey PRIMARY KEY (id);


--
-- Name: plans_goaltemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.plans_goaltemplate
    ADD CONSTRAINT plans_goaltemplate_pkey PRIMARY KEY (id);


--
-- Name: plans_infomessage_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.plans_infomessage
    ADD CONSTRAINT plans_infomessage_pkey PRIMARY KEY (id);


--
-- Name: plans_infomessagequeue_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.plans_infomessagequeue
    ADD CONSTRAINT plans_infomessagequeue_pkey PRIMARY KEY (id);


--
-- Name: plans_planconsent_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.plans_planconsent
    ADD CONSTRAINT plans_planconsent_pkey PRIMARY KEY (id);


--
-- Name: tasks_assessmentquestion_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_assessmentquestion
    ADD CONSTRAINT tasks_assessmentquestion_pkey PRIMARY KEY (id);


--
-- Name: tasks_assessmentresponse_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_assessmentresponse
    ADD CONSTRAINT tasks_assessmentresponse_pkey PRIMARY KEY (id);


--
-- Name: tasks_assessmenttaskinstance_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_assessmenttask
    ADD CONSTRAINT tasks_assessmenttaskinstance_pkey PRIMARY KEY (id);


--
-- Name: tasks_assessmenttasktemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_assessmenttasktemplate
    ADD CONSTRAINT tasks_assessmenttasktemplate_pkey PRIMARY KEY (id);


--
-- Name: tasks_medicationtaskinstance_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_medicationtask
    ADD CONSTRAINT tasks_medicationtaskinstance_pkey PRIMARY KEY (id);


--
-- Name: tasks_medicationtasktemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_medicationtasktemplate
    ADD CONSTRAINT tasks_medicationtasktemplate_pkey PRIMARY KEY (id);


--
-- Name: tasks_patienttaskinstance_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_patienttask
    ADD CONSTRAINT tasks_patienttaskinstance_pkey PRIMARY KEY (id);


--
-- Name: tasks_patienttasktemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_patienttasktemplate
    ADD CONSTRAINT tasks_patienttasktemplate_pkey PRIMARY KEY (id);


--
-- Name: tasks_symptomrating_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_symptomrating
    ADD CONSTRAINT tasks_symptomrating_pkey PRIMARY KEY (id);


--
-- Name: tasks_symptomtaskinstance_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_symptomtask
    ADD CONSTRAINT tasks_symptomtaskinstance_pkey PRIMARY KEY (id);


--
-- Name: tasks_symptomtasktemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_symptomtasktemplate
    ADD CONSTRAINT tasks_symptomtasktemplate_pkey PRIMARY KEY (id);


--
-- Name: tasks_teamtaskinstance_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_teamtask
    ADD CONSTRAINT tasks_teamtaskinstance_pkey PRIMARY KEY (id);


--
-- Name: tasks_teamtasktemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_teamtasktemplate
    ADD CONSTRAINT tasks_teamtasktemplate_pkey PRIMARY KEY (id);


--
-- Name: tasks_vitalquestion_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_vitalquestion
    ADD CONSTRAINT tasks_vitalquestion_pkey PRIMARY KEY (id);


--
-- Name: tasks_vitalresponse_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_vitalresponse
    ADD CONSTRAINT tasks_vitalresponse_pkey PRIMARY KEY (id);


--
-- Name: tasks_vitaltask_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_vitaltask
    ADD CONSTRAINT tasks_vitaltask_pkey PRIMARY KEY (id);


--
-- Name: tasks_vitaltasktemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

ALTER TABLE ONLY public.tasks_vitaltasktemplate
    ADD CONSTRAINT tasks_vitaltasktemplate_pkey PRIMARY KEY (id);


--
-- Name: account_emailaddress_email_03be32b2_like; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX account_emailaddress_email_03be32b2_like ON public.account_emailaddress USING btree (email varchar_pattern_ops);


--
-- Name: account_emailaddress_user_id_2c513194; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX account_emailaddress_user_id_2c513194 ON public.account_emailaddress USING btree (user_id);


--
-- Name: account_emailconfirmation_email_address_id_5b7f8c58; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX account_emailconfirmation_email_address_id_5b7f8c58 ON public.account_emailconfirmation USING btree (email_address_id);


--
-- Name: account_emailconfirmation_key_f43612bd_like; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX account_emailconfirmation_key_f43612bd_like ON public.account_emailconfirmation USING btree (key varchar_pattern_ops);


--
-- Name: accounts_emailuser_email_214aa4e3_like; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX accounts_emailuser_email_214aa4e3_like ON public.accounts_emailuser USING btree (email varchar_pattern_ops);


--
-- Name: accounts_emailuser_groups_emailuser_id_d8814aea; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX accounts_emailuser_groups_emailuser_id_d8814aea ON public.accounts_emailuser_groups USING btree (emailuser_id);


--
-- Name: accounts_emailuser_groups_group_id_87be9bed; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX accounts_emailuser_groups_group_id_87be9bed ON public.accounts_emailuser_groups USING btree (group_id);


--
-- Name: accounts_emailuser_user_permissions_emailuser_id_aa51241f; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX accounts_emailuser_user_permissions_emailuser_id_aa51241f ON public.accounts_emailuser_user_permissions USING btree (emailuser_id);


--
-- Name: accounts_emailuser_user_permissions_permission_id_884e7040; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX accounts_emailuser_user_permissions_permission_id_884e7040 ON public.accounts_emailuser_user_permissions USING btree (permission_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: core_employeeprofile_facil_employeeprofile_id_4a1fee35; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_facil_employeeprofile_id_4a1fee35 ON public.core_employeeprofile_facilities_managed USING btree (employeeprofile_id);


--
-- Name: core_employeeprofile_facilities_employeeprofile_id_d28ca144; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_facilities_employeeprofile_id_d28ca144 ON public.core_employeeprofile_facilities USING btree (employeeprofile_id);


--
-- Name: core_employeeprofile_facilities_facility_id_114bbdd4; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_facilities_facility_id_114bbdd4 ON public.core_employeeprofile_facilities USING btree (facility_id);


--
-- Name: core_employeeprofile_facilities_managed_facility_id_f14f9f6a; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_facilities_managed_facility_id_f14f9f6a ON public.core_employeeprofile_facilities_managed USING btree (facility_id);


--
-- Name: core_employeeprofile_organ_employeeprofile_id_79a27cac; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_organ_employeeprofile_id_79a27cac ON public.core_employeeprofile_organizations_managed USING btree (employeeprofile_id);


--
-- Name: core_employeeprofile_organ_organization_id_4a250075; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_organ_organization_id_4a250075 ON public.core_employeeprofile_organizations_managed USING btree (organization_id);


--
-- Name: core_employeeprofile_organizations_employeeprofile_id_98930f29; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_organizations_employeeprofile_id_98930f29 ON public.core_employeeprofile_organizations USING btree (employeeprofile_id);


--
-- Name: core_employeeprofile_organizations_organization_id_52e176ba; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_organizations_organization_id_52e176ba ON public.core_employeeprofile_organizations USING btree (organization_id);


--
-- Name: core_employeeprofile_roles_employeeprofile_id_13cc57f2; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_roles_employeeprofile_id_13cc57f2 ON public.core_employeeprofile_roles USING btree (employeeprofile_id);


--
-- Name: core_employeeprofile_roles_providerrole_id_0de51ff8; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_roles_providerrole_id_0de51ff8 ON public.core_employeeprofile_roles USING btree (providerrole_id);


--
-- Name: core_employeeprofile_specialty_id_bab4037b; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_specialty_id_bab4037b ON public.core_employeeprofile USING btree (specialty_id);


--
-- Name: core_employeeprofile_title_id_ff3cb4f1; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_employeeprofile_title_id_ff3cb4f1 ON public.core_employeeprofile USING btree (title_id);


--
-- Name: core_facility_organization_id_bd747882; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX core_facility_organization_id_bd747882 ON public.core_facility USING btree (organization_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: patients_patientdiagnosis_diagnosis_id_48f4f8e3; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientdiagnosis_diagnosis_id_48f4f8e3 ON public.patients_patientdiagnosis USING btree (diagnosis_id);


--
-- Name: patients_patientdiagnosis_patient_id_2f907c20; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientdiagnosis_patient_id_2f907c20 ON public.patients_patientdiagnosis USING btree (patient_id);


--
-- Name: patients_patientmedication_medication_id_e5b51fd5; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientmedication_medication_id_e5b51fd5 ON public.patients_patientmedication USING btree (medication_id);


--
-- Name: patients_patientmedication_patient_id_3749b9e9; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientmedication_patient_id_3749b9e9 ON public.patients_patientmedication USING btree (patient_id);


--
-- Name: patients_patientmedication_prescribing_practitioner_id_6df55925; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientmedication_prescribing_practitioner_id_6df55925 ON public.patients_patientmedication USING btree (prescribing_practitioner_id);


--
-- Name: patients_patientprocedure_patient_id_b02b1da6; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientprocedure_patient_id_b02b1da6 ON public.patients_patientprocedure USING btree (patient_id);


--
-- Name: patients_patientprocedure_procedure_id_29da7031; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientprocedure_procedure_id_29da7031 ON public.patients_patientprocedure USING btree (procedure_id);


--
-- Name: patients_patientprofile_diagnosis_patientdiagnosis_id_a0279a8a; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientprofile_diagnosis_patientdiagnosis_id_a0279a8a ON public.patients_patientprofile_diagnosis USING btree (patientdiagnosis_id);


--
-- Name: patients_patientprofile_diagnosis_patientprofile_id_40c062ac; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientprofile_diagnosis_patientprofile_id_40c062ac ON public.patients_patientprofile_diagnosis USING btree (patientprofile_id);


--
-- Name: patients_patientprofile_facility_id_fa6f7389; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientprofile_facility_id_fa6f7389 ON public.patients_patientprofile USING btree (facility_id);


--
-- Name: patients_patientprofile_message_for_day_id_d7f260ea; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientprofile_message_for_day_id_d7f260ea ON public.patients_patientprofile USING btree (message_for_day_id);


--
-- Name: patients_patientverificationcode_patient_id_ba680c23; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_patientverificationcode_patient_id_ba680c23 ON public.patients_patientverificationcode USING btree (patient_id);


--
-- Name: patients_potentialpatient_facility_facility_id_22513112; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_potentialpatient_facility_facility_id_22513112 ON public.patients_potentialpatient_facility USING btree (facility_id);


--
-- Name: patients_potentialpatient_facility_potentialpatient_id_85845ab5; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_potentialpatient_facility_potentialpatient_id_85845ab5 ON public.patients_potentialpatient_facility USING btree (potentialpatient_id);


--
-- Name: patients_problemarea_identified_by_id_1314730e; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_problemarea_identified_by_id_1314730e ON public.patients_problemarea USING btree (identified_by_id);


--
-- Name: patients_problemarea_patient_id_2f944c0a; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_problemarea_patient_id_2f944c0a ON public.patients_problemarea USING btree (patient_id);


--
-- Name: patients_reminderemail_patient_id_6119ba2c; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX patients_reminderemail_patient_id_6119ba2c ON public.patients_reminderemail USING btree (patient_id);


--
-- Name: plans_careplaninstance_patient_id_18977d37; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_careplaninstance_patient_id_18977d37 ON public.plans_careplan USING btree (patient_id);


--
-- Name: plans_careplaninstance_plan_template_id_92b7576c; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_careplaninstance_plan_template_id_92b7576c ON public.plans_careplan USING btree (plan_template_id);


--
-- Name: plans_careteammember_employee_profile_id_1be00d1e; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_careteammember_employee_profile_id_1be00d1e ON public.plans_careteammember USING btree (employee_profile_id);


--
-- Name: plans_careteammember_plan_instance_id_a567df6b; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_careteammember_plan_instance_id_a567df6b ON public.plans_careteammember USING btree (plan_id);


--
-- Name: plans_careteammember_role_id_5fcbda8e; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_careteammember_role_id_5fcbda8e ON public.plans_careteammember USING btree (role_id);


--
-- Name: plans_goal_goal_template_id_4c8ac040; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_goal_goal_template_id_4c8ac040 ON public.plans_goal USING btree (goal_template_id);


--
-- Name: plans_goal_plan_id_62ddc712; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_goal_plan_id_62ddc712 ON public.plans_goal USING btree (plan_id);


--
-- Name: plans_goalcomment_goal_id_6d0c18f7; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_goalcomment_goal_id_6d0c18f7 ON public.plans_goalcomment USING btree (goal_id);


--
-- Name: plans_goalcomment_user_id_85d2a63d; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_goalcomment_user_id_85d2a63d ON public.plans_goalcomment USING btree (user_id);


--
-- Name: plans_goalprogress_goal_id_00fa5980; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_goalprogress_goal_id_00fa5980 ON public.plans_goalprogress USING btree (goal_id);


--
-- Name: plans_goaltemplate_plan_template_id_839d0290; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_goaltemplate_plan_template_id_839d0290 ON public.plans_goaltemplate USING btree (plan_template_id);


--
-- Name: plans_infomessage_queue_id_524fa9e2; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_infomessage_queue_id_524fa9e2 ON public.plans_infomessage USING btree (queue_id);


--
-- Name: plans_infomessagequeue_plan_template_id_83f05613; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_infomessagequeue_plan_template_id_83f05613 ON public.plans_infomessagequeue USING btree (plan_template_id);


--
-- Name: plans_planconsent_plan_instance_id_5a370b76; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX plans_planconsent_plan_instance_id_5a370b76 ON public.plans_planconsent USING btree (plan_id);


--
-- Name: tasks_assessmentquestion_assessment_task_template_id_3d44c73b; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_assessmentquestion_assessment_task_template_id_3d44c73b ON public.tasks_assessmentquestion USING btree (assessment_task_template_id);


--
-- Name: tasks_assessmentresponse_assessment_question_id_eea7b51c; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_assessmentresponse_assessment_question_id_eea7b51c ON public.tasks_assessmentresponse USING btree (assessment_question_id);


--
-- Name: tasks_assessmentresponse_assessment_task_instance_id_6198b0e3; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_assessmentresponse_assessment_task_instance_id_6198b0e3 ON public.tasks_assessmentresponse USING btree (assessment_task_id);


--
-- Name: tasks_assessmenttaskinstan_assessment_task_template_i_2931fa40; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_assessmenttaskinstan_assessment_task_template_i_2931fa40 ON public.tasks_assessmenttask USING btree (assessment_task_template_id);


--
-- Name: tasks_assessmenttaskinstance_plan_instance_id_9e5fdcb5; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_assessmenttaskinstance_plan_instance_id_9e5fdcb5 ON public.tasks_assessmenttask USING btree (plan_id);


--
-- Name: tasks_assessmenttasktemplate_plan_template_id_bf6811bd; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_assessmenttasktemplate_plan_template_id_bf6811bd ON public.tasks_assessmenttasktemplate USING btree (plan_template_id);


--
-- Name: tasks_medicationtaskinstan_medication_task_template_i_6a0fa8d0; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_medicationtaskinstan_medication_task_template_i_6a0fa8d0 ON public.tasks_medicationtask USING btree (medication_task_template_id);


--
-- Name: tasks_medicationtasktemplate_patient_medication_id_90f3f071; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_medicationtasktemplate_patient_medication_id_90f3f071 ON public.tasks_medicationtasktemplate USING btree (patient_medication_id);


--
-- Name: tasks_medicationtasktemplate_plan_instance_id_c8812960; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_medicationtasktemplate_plan_instance_id_c8812960 ON public.tasks_medicationtasktemplate USING btree (plan_id);


--
-- Name: tasks_patienttaskinstance_patient_task_template_id_65b392ca; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_patienttaskinstance_patient_task_template_id_65b392ca ON public.tasks_patienttask USING btree (patient_task_template_id);


--
-- Name: tasks_patienttaskinstance_plan_instance_id_d4afdc18; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_patienttaskinstance_plan_instance_id_d4afdc18 ON public.tasks_patienttask USING btree (plan_id);


--
-- Name: tasks_patienttasktemplate_plan_template_id_ea4548f3; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_patienttasktemplate_plan_template_id_ea4548f3 ON public.tasks_patienttasktemplate USING btree (plan_template_id);


--
-- Name: tasks_symptomrating_symptom_id_be0d83a8; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_symptomrating_symptom_id_be0d83a8 ON public.tasks_symptomrating USING btree (symptom_id);


--
-- Name: tasks_symptomrating_symptom_task_instance_id_853419df; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_symptomrating_symptom_task_instance_id_853419df ON public.tasks_symptomrating USING btree (symptom_task_id);


--
-- Name: tasks_symptomtaskinstance_plan_instance_id_443a88e7; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_symptomtaskinstance_plan_instance_id_443a88e7 ON public.tasks_symptomtask USING btree (plan_id);


--
-- Name: tasks_symptomtaskinstance_symptom_task_template_id_8fa0c19e; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_symptomtaskinstance_symptom_task_template_id_8fa0c19e ON public.tasks_symptomtask USING btree (symptom_task_template_id);


--
-- Name: tasks_symptomtasktemplate_plan_template_id_25001518; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_symptomtasktemplate_plan_template_id_25001518 ON public.tasks_symptomtasktemplate USING btree (plan_template_id);


--
-- Name: tasks_teamtaskinstance_plan_instance_id_6c542de7; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_teamtaskinstance_plan_instance_id_6c542de7 ON public.tasks_teamtask USING btree (plan_id);


--
-- Name: tasks_teamtaskinstance_team_task_template_id_1fc6a06f; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_teamtaskinstance_team_task_template_id_1fc6a06f ON public.tasks_teamtask USING btree (team_task_template_id);


--
-- Name: tasks_teamtasktemplate_plan_template_id_532180d9; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_teamtasktemplate_plan_template_id_532180d9 ON public.tasks_teamtasktemplate USING btree (plan_template_id);


--
-- Name: tasks_teamtasktemplate_role_id_424c035e; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_teamtasktemplate_role_id_424c035e ON public.tasks_teamtasktemplate USING btree (role_id);


--
-- Name: tasks_vitalquestion_vital_task_template_id_fa87b904; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_vitalquestion_vital_task_template_id_fa87b904 ON public.tasks_vitalquestion USING btree (vital_task_template_id);


--
-- Name: tasks_vitalresponse_question_id_d601c979; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_vitalresponse_question_id_d601c979 ON public.tasks_vitalresponse USING btree (question_id);


--
-- Name: tasks_vitalresponse_vital_task_id_a6679538; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_vitalresponse_vital_task_id_a6679538 ON public.tasks_vitalresponse USING btree (vital_task_id);


--
-- Name: tasks_vitaltask_plan_id_4ccf7c29; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_vitaltask_plan_id_4ccf7c29 ON public.tasks_vitaltask USING btree (plan_id);


--
-- Name: tasks_vitaltask_vital_task_template_id_93334ba8; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_vitaltask_vital_task_template_id_93334ba8 ON public.tasks_vitaltask USING btree (vital_task_template_id);


--
-- Name: tasks_vitaltasktemplate_plan_template_id_ac713322; Type: INDEX; Schema: public; Owner: care_adopt_backend; Tablespace: 
--

CREATE INDEX tasks_vitaltasktemplate_plan_template_id_ac713322 ON public.tasks_vitaltasktemplate USING btree (plan_template_id);


--
-- Name: account_emailaddress_user_id_2c513194_fk_accounts_emailuser_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_2c513194_fk_accounts_emailuser_id FOREIGN KEY (user_id) REFERENCES public.accounts_emailuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_emailconfirm_email_address_id_5b7f8c58_fk_account_e; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirm_email_address_id_5b7f8c58_fk_account_e FOREIGN KEY (email_address_id) REFERENCES public.account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_emailuser_g_emailuser_id_d8814aea_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.accounts_emailuser_groups
    ADD CONSTRAINT accounts_emailuser_g_emailuser_id_d8814aea_fk_accounts_ FOREIGN KEY (emailuser_id) REFERENCES public.accounts_emailuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_emailuser_groups_group_id_87be9bed_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.accounts_emailuser_groups
    ADD CONSTRAINT accounts_emailuser_groups_group_id_87be9bed_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_emailuser_u_emailuser_id_aa51241f_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.accounts_emailuser_user_permissions
    ADD CONSTRAINT accounts_emailuser_u_emailuser_id_aa51241f_fk_accounts_ FOREIGN KEY (emailuser_id) REFERENCES public.accounts_emailuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_emailuser_u_permission_id_884e7040_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.accounts_emailuser_user_permissions
    ADD CONSTRAINT accounts_emailuser_u_permission_id_884e7040_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token_user_id_35299eff_fk_accounts_emailuser_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_accounts_emailuser_id FOREIGN KEY (user_id) REFERENCES public.accounts_emailuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_employeeprofile_id_13cc57f2_fk_core_empl; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_roles
    ADD CONSTRAINT core_employeeprofile_employeeprofile_id_13cc57f2_fk_core_empl FOREIGN KEY (employeeprofile_id) REFERENCES public.core_employeeprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_employeeprofile_id_4a1fee35_fk_core_empl; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_facilities_managed
    ADD CONSTRAINT core_employeeprofile_employeeprofile_id_4a1fee35_fk_core_empl FOREIGN KEY (employeeprofile_id) REFERENCES public.core_employeeprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_employeeprofile_id_79a27cac_fk_core_empl; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_organizations_managed
    ADD CONSTRAINT core_employeeprofile_employeeprofile_id_79a27cac_fk_core_empl FOREIGN KEY (employeeprofile_id) REFERENCES public.core_employeeprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_employeeprofile_id_98930f29_fk_core_empl; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_organizations
    ADD CONSTRAINT core_employeeprofile_employeeprofile_id_98930f29_fk_core_empl FOREIGN KEY (employeeprofile_id) REFERENCES public.core_employeeprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_employeeprofile_id_d28ca144_fk_core_empl; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_facilities
    ADD CONSTRAINT core_employeeprofile_employeeprofile_id_d28ca144_fk_core_empl FOREIGN KEY (employeeprofile_id) REFERENCES public.core_employeeprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_facility_id_114bbdd4_fk_core_faci; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_facilities
    ADD CONSTRAINT core_employeeprofile_facility_id_114bbdd4_fk_core_faci FOREIGN KEY (facility_id) REFERENCES public.core_facility(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_facility_id_f14f9f6a_fk_core_faci; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_facilities_managed
    ADD CONSTRAINT core_employeeprofile_facility_id_f14f9f6a_fk_core_faci FOREIGN KEY (facility_id) REFERENCES public.core_facility(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_organization_id_4a250075_fk_core_orga; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_organizations_managed
    ADD CONSTRAINT core_employeeprofile_organization_id_4a250075_fk_core_orga FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_organization_id_52e176ba_fk_core_orga; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_organizations
    ADD CONSTRAINT core_employeeprofile_organization_id_52e176ba_fk_core_orga FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_providerrole_id_0de51ff8_fk_core_prov; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile_roles
    ADD CONSTRAINT core_employeeprofile_providerrole_id_0de51ff8_fk_core_prov FOREIGN KEY (providerrole_id) REFERENCES public.core_providerrole(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_specialty_id_bab4037b_fk_core_prov; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile
    ADD CONSTRAINT core_employeeprofile_specialty_id_bab4037b_fk_core_prov FOREIGN KEY (specialty_id) REFERENCES public.core_providerspecialty(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_title_id_ff3cb4f1_fk_core_providertitle_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile
    ADD CONSTRAINT core_employeeprofile_title_id_ff3cb4f1_fk_core_providertitle_id FOREIGN KEY (title_id) REFERENCES public.core_providertitle(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_employeeprofile_user_id_64abf4fb_fk_accounts_emailuser_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_employeeprofile
    ADD CONSTRAINT core_employeeprofile_user_id_64abf4fb_fk_accounts_emailuser_id FOREIGN KEY (user_id) REFERENCES public.accounts_emailuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_facility_organization_id_bd747882_fk_core_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.core_facility
    ADD CONSTRAINT core_facility_organization_id_bd747882_fk_core_organization_id FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_c564eba6_fk_accounts_emailuser_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_accounts_emailuser_id FOREIGN KEY (user_id) REFERENCES public.accounts_emailuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientdiag_diagnosis_id_48f4f8e3_fk_core_diag; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientdiagnosis
    ADD CONSTRAINT patients_patientdiag_diagnosis_id_48f4f8e3_fk_core_diag FOREIGN KEY (diagnosis_id) REFERENCES public.core_diagnosis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientdiag_patient_id_2f907c20_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientdiagnosis
    ADD CONSTRAINT patients_patientdiag_patient_id_2f907c20_fk_patients_ FOREIGN KEY (patient_id) REFERENCES public.patients_patientprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientmedi_medication_id_e5b51fd5_fk_core_medi; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientmedication
    ADD CONSTRAINT patients_patientmedi_medication_id_e5b51fd5_fk_core_medi FOREIGN KEY (medication_id) REFERENCES public.core_medication(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientmedi_patient_id_3749b9e9_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientmedication
    ADD CONSTRAINT patients_patientmedi_patient_id_3749b9e9_fk_patients_ FOREIGN KEY (patient_id) REFERENCES public.patients_patientprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientmedi_prescribing_practiti_6df55925_fk_core_empl; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientmedication
    ADD CONSTRAINT patients_patientmedi_prescribing_practiti_6df55925_fk_core_empl FOREIGN KEY (prescribing_practitioner_id) REFERENCES public.core_employeeprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientproc_patient_id_b02b1da6_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientprocedure
    ADD CONSTRAINT patients_patientproc_patient_id_b02b1da6_fk_patients_ FOREIGN KEY (patient_id) REFERENCES public.patients_patientprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientproc_procedure_id_29da7031_fk_core_proc; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientprocedure
    ADD CONSTRAINT patients_patientproc_procedure_id_29da7031_fk_core_proc FOREIGN KEY (procedure_id) REFERENCES public.core_procedure(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientprof_facility_id_fa6f7389_fk_core_faci; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientprofile
    ADD CONSTRAINT patients_patientprof_facility_id_fa6f7389_fk_core_faci FOREIGN KEY (facility_id) REFERENCES public.core_facility(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientprof_message_for_day_id_d7f260ea_fk_plans_inf; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientprofile
    ADD CONSTRAINT patients_patientprof_message_for_day_id_d7f260ea_fk_plans_inf FOREIGN KEY (message_for_day_id) REFERENCES public.plans_infomessage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientprof_patientdiagnosis_id_a0279a8a_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientprofile_diagnosis
    ADD CONSTRAINT patients_patientprof_patientdiagnosis_id_a0279a8a_fk_patients_ FOREIGN KEY (patientdiagnosis_id) REFERENCES public.patients_patientdiagnosis(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientprof_patientprofile_id_40c062ac_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientprofile_diagnosis
    ADD CONSTRAINT patients_patientprof_patientprofile_id_40c062ac_fk_patients_ FOREIGN KEY (patientprofile_id) REFERENCES public.patients_patientprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientprof_user_id_61c3977d_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientprofile
    ADD CONSTRAINT patients_patientprof_user_id_61c3977d_fk_accounts_ FOREIGN KEY (user_id) REFERENCES public.accounts_emailuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_patientveri_patient_id_ba680c23_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_patientverificationcode
    ADD CONSTRAINT patients_patientveri_patient_id_ba680c23_fk_patients_ FOREIGN KEY (patient_id) REFERENCES public.patients_patientprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_potentialpa_facility_id_22513112_fk_core_faci; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_potentialpatient_facility
    ADD CONSTRAINT patients_potentialpa_facility_id_22513112_fk_core_faci FOREIGN KEY (facility_id) REFERENCES public.core_facility(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_potentialpa_patient_profile_id_1a79a87f_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_potentialpatient
    ADD CONSTRAINT patients_potentialpa_patient_profile_id_1a79a87f_fk_patients_ FOREIGN KEY (patient_profile_id) REFERENCES public.patients_patientprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_potentialpa_potentialpatient_id_85845ab5_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_potentialpatient_facility
    ADD CONSTRAINT patients_potentialpa_potentialpatient_id_85845ab5_fk_patients_ FOREIGN KEY (potentialpatient_id) REFERENCES public.patients_potentialpatient(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_problemarea_identified_by_id_1314730e_fk_core_empl; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_problemarea
    ADD CONSTRAINT patients_problemarea_identified_by_id_1314730e_fk_core_empl FOREIGN KEY (identified_by_id) REFERENCES public.core_employeeprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_problemarea_patient_id_2f944c0a_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_problemarea
    ADD CONSTRAINT patients_problemarea_patient_id_2f944c0a_fk_patients_ FOREIGN KEY (patient_id) REFERENCES public.patients_patientprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: patients_reminderema_patient_id_6119ba2c_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.patients_reminderemail
    ADD CONSTRAINT patients_reminderema_patient_id_6119ba2c_fk_patients_ FOREIGN KEY (patient_id) REFERENCES public.patients_patientprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_careplan_plan_template_id_7e4091e2_fk_plans_car; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_careplan
    ADD CONSTRAINT plans_careplan_plan_template_id_7e4091e2_fk_plans_car FOREIGN KEY (plan_template_id) REFERENCES public.plans_careplantemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_careplaninstan_patient_id_18977d37_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_careplan
    ADD CONSTRAINT plans_careplaninstan_patient_id_18977d37_fk_patients_ FOREIGN KEY (patient_id) REFERENCES public.patients_patientprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_careteammember_employee_profile_id_1be00d1e_fk_core_empl; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_careteammember
    ADD CONSTRAINT plans_careteammember_employee_profile_id_1be00d1e_fk_core_empl FOREIGN KEY (employee_profile_id) REFERENCES public.core_employeeprofile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_careteammember_plan_id_adfb2c91_fk_plans_careplan_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_careteammember
    ADD CONSTRAINT plans_careteammember_plan_id_adfb2c91_fk_plans_careplan_id FOREIGN KEY (plan_id) REFERENCES public.plans_careplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_careteammember_role_id_5fcbda8e_fk_core_providerrole_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_careteammember
    ADD CONSTRAINT plans_careteammember_role_id_5fcbda8e_fk_core_providerrole_id FOREIGN KEY (role_id) REFERENCES public.core_providerrole(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_goal_goal_template_id_4c8ac040_fk_plans_goaltemplate_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_goal
    ADD CONSTRAINT plans_goal_goal_template_id_4c8ac040_fk_plans_goaltemplate_id FOREIGN KEY (goal_template_id) REFERENCES public.plans_goaltemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_goal_plan_id_62ddc712_fk_plans_careplan_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_goal
    ADD CONSTRAINT plans_goal_plan_id_62ddc712_fk_plans_careplan_id FOREIGN KEY (plan_id) REFERENCES public.plans_careplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_goalcomment_goal_id_6d0c18f7_fk_plans_goal_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_goalcomment
    ADD CONSTRAINT plans_goalcomment_goal_id_6d0c18f7_fk_plans_goal_id FOREIGN KEY (goal_id) REFERENCES public.plans_goal(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_goalcomment_user_id_85d2a63d_fk_accounts_emailuser_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_goalcomment
    ADD CONSTRAINT plans_goalcomment_user_id_85d2a63d_fk_accounts_emailuser_id FOREIGN KEY (user_id) REFERENCES public.accounts_emailuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_goalprogress_goal_id_00fa5980_fk_plans_goal_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_goalprogress
    ADD CONSTRAINT plans_goalprogress_goal_id_00fa5980_fk_plans_goal_id FOREIGN KEY (goal_id) REFERENCES public.plans_goal(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_goaltemplate_plan_template_id_839d0290_fk_plans_car; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_goaltemplate
    ADD CONSTRAINT plans_goaltemplate_plan_template_id_839d0290_fk_plans_car FOREIGN KEY (plan_template_id) REFERENCES public.plans_careplantemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_infomessage_queue_id_524fa9e2_fk_plans_inf; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_infomessage
    ADD CONSTRAINT plans_infomessage_queue_id_524fa9e2_fk_plans_inf FOREIGN KEY (queue_id) REFERENCES public.plans_infomessagequeue(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_infomessageque_plan_template_id_83f05613_fk_plans_car; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_infomessagequeue
    ADD CONSTRAINT plans_infomessageque_plan_template_id_83f05613_fk_plans_car FOREIGN KEY (plan_template_id) REFERENCES public.plans_careplantemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: plans_planconsent_plan_id_46860b56_fk_plans_careplan_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.plans_planconsent
    ADD CONSTRAINT plans_planconsent_plan_id_46860b56_fk_plans_careplan_id FOREIGN KEY (plan_id) REFERENCES public.plans_careplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_assessmentques_assessment_task_temp_3d44c73b_fk_tasks_ass; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_assessmentquestion
    ADD CONSTRAINT tasks_assessmentques_assessment_task_temp_3d44c73b_fk_tasks_ass FOREIGN KEY (assessment_task_template_id) REFERENCES public.tasks_assessmenttasktemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_assessmentresp_assessment_question__eea7b51c_fk_tasks_ass; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_assessmentresponse
    ADD CONSTRAINT tasks_assessmentresp_assessment_question__eea7b51c_fk_tasks_ass FOREIGN KEY (assessment_question_id) REFERENCES public.tasks_assessmentquestion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_assessmentresp_assessment_task_id_a9377756_fk_tasks_ass; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_assessmentresponse
    ADD CONSTRAINT tasks_assessmentresp_assessment_task_id_a9377756_fk_tasks_ass FOREIGN KEY (assessment_task_id) REFERENCES public.tasks_assessmenttask(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_assessmenttask_assessment_task_temp_2931fa40_fk_tasks_ass; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_assessmenttask
    ADD CONSTRAINT tasks_assessmenttask_assessment_task_temp_2931fa40_fk_tasks_ass FOREIGN KEY (assessment_task_template_id) REFERENCES public.tasks_assessmenttasktemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_assessmenttask_plan_id_bc81eaf0_fk_plans_careplan_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_assessmenttask
    ADD CONSTRAINT tasks_assessmenttask_plan_id_bc81eaf0_fk_plans_careplan_id FOREIGN KEY (plan_id) REFERENCES public.plans_careplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_assessmenttask_plan_template_id_bf6811bd_fk_plans_car; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_assessmenttasktemplate
    ADD CONSTRAINT tasks_assessmenttask_plan_template_id_bf6811bd_fk_plans_car FOREIGN KEY (plan_template_id) REFERENCES public.plans_careplantemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_medicationtask_medication_task_temp_85120fa3_fk_tasks_med; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_medicationtask
    ADD CONSTRAINT tasks_medicationtask_medication_task_temp_85120fa3_fk_tasks_med FOREIGN KEY (medication_task_template_id) REFERENCES public.tasks_medicationtasktemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_medicationtask_patient_medication_i_90f3f071_fk_patients_; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_medicationtasktemplate
    ADD CONSTRAINT tasks_medicationtask_patient_medication_i_90f3f071_fk_patients_ FOREIGN KEY (patient_medication_id) REFERENCES public.patients_patientmedication(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_medicationtask_plan_id_d232da9a_fk_plans_car; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_medicationtasktemplate
    ADD CONSTRAINT tasks_medicationtask_plan_id_d232da9a_fk_plans_car FOREIGN KEY (plan_id) REFERENCES public.plans_careplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_patienttask_plan_id_3c4e2ab9_fk_plans_careplan_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_patienttask
    ADD CONSTRAINT tasks_patienttask_plan_id_3c4e2ab9_fk_plans_careplan_id FOREIGN KEY (plan_id) REFERENCES public.plans_careplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_patienttaskins_patient_task_templat_65b392ca_fk_tasks_pat; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_patienttask
    ADD CONSTRAINT tasks_patienttaskins_patient_task_templat_65b392ca_fk_tasks_pat FOREIGN KEY (patient_task_template_id) REFERENCES public.tasks_patienttasktemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_patienttasktem_plan_template_id_ea4548f3_fk_plans_car; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_patienttasktemplate
    ADD CONSTRAINT tasks_patienttasktem_plan_template_id_ea4548f3_fk_plans_car FOREIGN KEY (plan_template_id) REFERENCES public.plans_careplantemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_symptomrating_symptom_id_be0d83a8_fk_core_symptom_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_symptomrating
    ADD CONSTRAINT tasks_symptomrating_symptom_id_be0d83a8_fk_core_symptom_id FOREIGN KEY (symptom_id) REFERENCES public.core_symptom(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_symptomrating_symptom_task_id_0ff82824_fk_tasks_sym; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_symptomrating
    ADD CONSTRAINT tasks_symptomrating_symptom_task_id_0ff82824_fk_tasks_sym FOREIGN KEY (symptom_task_id) REFERENCES public.tasks_symptomtask(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_symptomtask_plan_id_2f87e903_fk_plans_careplan_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_symptomtask
    ADD CONSTRAINT tasks_symptomtask_plan_id_2f87e903_fk_plans_careplan_id FOREIGN KEY (plan_id) REFERENCES public.plans_careplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_symptomtaskins_symptom_task_templat_8fa0c19e_fk_tasks_sym; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_symptomtask
    ADD CONSTRAINT tasks_symptomtaskins_symptom_task_templat_8fa0c19e_fk_tasks_sym FOREIGN KEY (symptom_task_template_id) REFERENCES public.tasks_symptomtasktemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_symptomtasktem_plan_template_id_25001518_fk_plans_car; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_symptomtasktemplate
    ADD CONSTRAINT tasks_symptomtasktem_plan_template_id_25001518_fk_plans_car FOREIGN KEY (plan_template_id) REFERENCES public.plans_careplantemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_teamtask_plan_id_22a8c7bc_fk_plans_careplan_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_teamtask
    ADD CONSTRAINT tasks_teamtask_plan_id_22a8c7bc_fk_plans_careplan_id FOREIGN KEY (plan_id) REFERENCES public.plans_careplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_teamtaskinstan_team_task_template_i_1fc6a06f_fk_tasks_tea; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_teamtask
    ADD CONSTRAINT tasks_teamtaskinstan_team_task_template_i_1fc6a06f_fk_tasks_tea FOREIGN KEY (team_task_template_id) REFERENCES public.tasks_teamtasktemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_teamtasktempla_plan_template_id_532180d9_fk_plans_car; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_teamtasktemplate
    ADD CONSTRAINT tasks_teamtasktempla_plan_template_id_532180d9_fk_plans_car FOREIGN KEY (plan_template_id) REFERENCES public.plans_careplantemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_teamtasktemplate_role_id_424c035e_fk_core_providerrole_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_teamtasktemplate
    ADD CONSTRAINT tasks_teamtasktemplate_role_id_424c035e_fk_core_providerrole_id FOREIGN KEY (role_id) REFERENCES public.core_providerrole(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_vitalquestion_vital_task_template__fa87b904_fk_tasks_vit; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_vitalquestion
    ADD CONSTRAINT tasks_vitalquestion_vital_task_template__fa87b904_fk_tasks_vit FOREIGN KEY (vital_task_template_id) REFERENCES public.tasks_vitaltasktemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_vitalresponse_question_id_d601c979_fk_tasks_vit; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_vitalresponse
    ADD CONSTRAINT tasks_vitalresponse_question_id_d601c979_fk_tasks_vit FOREIGN KEY (question_id) REFERENCES public.tasks_vitalquestion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_vitalresponse_vital_task_id_a6679538_fk_tasks_vit; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_vitalresponse
    ADD CONSTRAINT tasks_vitalresponse_vital_task_id_a6679538_fk_tasks_vit FOREIGN KEY (vital_task_id) REFERENCES public.tasks_vitaltask(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_vitaltask_plan_id_4ccf7c29_fk_plans_careplan_id; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_vitaltask
    ADD CONSTRAINT tasks_vitaltask_plan_id_4ccf7c29_fk_plans_careplan_id FOREIGN KEY (plan_id) REFERENCES public.plans_careplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_vitaltask_vital_task_template__93334ba8_fk_tasks_vit; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_vitaltask
    ADD CONSTRAINT tasks_vitaltask_vital_task_template__93334ba8_fk_tasks_vit FOREIGN KEY (vital_task_template_id) REFERENCES public.tasks_vitaltasktemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_vitaltasktempl_plan_template_id_ac713322_fk_plans_car; Type: FK CONSTRAINT; Schema: public; Owner: care_adopt_backend
--

ALTER TABLE ONLY public.tasks_vitaltasktemplate
    ADD CONSTRAINT tasks_vitaltasktempl_plan_template_id_ac713322_fk_plans_car FOREIGN KEY (plan_template_id) REFERENCES public.plans_careplantemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

