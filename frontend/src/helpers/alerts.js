import Alert from "react-s-alert";

export const showSuccess = message =>
  Alert.success(message, {
    position: "bottom-right",
    effect: "slide",
    html: false
  });

export const showError = message => {
  console.error(message);
  Alert.error(message, {
    timeout: 10000,
    effect: "slide",
    position: "bottom-right"
  });
};
