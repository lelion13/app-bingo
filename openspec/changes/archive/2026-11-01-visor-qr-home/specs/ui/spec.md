# Delta for UI

## ADDED Requirements

### Requirement: Production visor QR on home

The home page MUST display a QR code in the left control column, below the primary action buttons. The QR MUST encode exactly `https://bingo.lionapp.cloud/visor`. The rendered QR SHOULD be approximately 120px wide (small).

#### Scenario: Scan opens production visor

- GIVEN the home page is loaded (any host)
- WHEN a device scans the displayed QR
- THEN it MUST open `https://bingo.lionapp.cloud/visor`
- AND MUST NOT encode the current page origin instead of production

### Requirement: Friendly visor link on home

Adjacent to the QR (same left-column block), the home page MUST show a clickable link whose visible text is `bingo.lionapp.cloud/visor` and whose `href` is `https://bingo.lionapp.cloud/visor`.

#### Scenario: Tap friendly link

- GIVEN the home page is loaded
- WHEN the user activates the friendly link
- THEN the browser MUST navigate to `https://bingo.lionapp.cloud/visor`

## MODIFIED Requirements

### Requirement: Home discovers viewer

(Previously: home MUST include a Visor button/link control.)

The home page MUST discover the viewer via the production QR and friendly link described above. A separate **Visor** button control MUST NOT be shown.

#### Scenario: No Visor button

- GIVEN the home page is loaded
- WHEN the operator inspects the left controls
- THEN there MUST NOT be a standalone “Visor” button
- AND the QR + friendly link block MUST be present below the remaining actions
