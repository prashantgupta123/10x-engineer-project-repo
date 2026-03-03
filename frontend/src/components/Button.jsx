export const Button = ({ children, variant = 'primary', onClick, type = 'button', disabled }) => (
  <button
    type={type}
    onClick={onClick}
    disabled={disabled}
    className={`btn btn-${variant}`}
  >
    {children}
  </button>
);
