import { describe, it, expect, vi } from 'vitest'
import { render } from '@testing-library/vue'
import LeavingTitle from '../LeavingTitle.vue'

describe('LeavingTitle', () => {
  beforeEach(() => {
    // Mock date to ensure future dates are always "upcoming"
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2024-12-31'))
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('renders titles correctly', () => {
    const titles = ['Movie 1', 'Movie 2']
    const date = '2025-01-01'
    
    const { container } = render(LeavingTitle, {
      props: {
        date,
        titles
      },
      global: {
        provide: {
          userTimezone: 'UTC'
        }
      }
    })

    // Check if the date is rendered (more flexible approach)
    expect(container.textContent).toContain('01 January 2025')
    
    // Check if titles are rendered
    expect(container.textContent).toContain('Movie 1')
    expect(container.textContent).toContain('Movie 2')
  })

  it('removes duplicate titles', () => {
    const titles = ['Movie 1', 'Movie 1', 'Movie 2']
    const date = '2025-01-01'
    
    const { getAllByText } = render(LeavingTitle, {
      props: {
        date,
        titles
      },
      global: {
        provide: {
          userTimezone: 'UTC'
        }
      }
    })

    // Use getAllByText to check for duplicate elements
    const movieElements = getAllByText('Movie 1')
    expect(movieElements).toHaveLength(1)
  })

  it('does not render past dates', () => {
    const titles = ['Movie 1']
    const date = '2024-01-01' // Past date
    
    const { container } = render(LeavingTitle, {
      props: {
        date,
        titles
      },
      global: {
        provide: {
          userTimezone: 'UTC'
        }
      }
    })

    expect(container.textContent).toBe('')
  })
}) 